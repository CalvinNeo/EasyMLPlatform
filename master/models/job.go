// job
package models

import (
	"errors"

	"github.com/astaxie/beego/orm"
)

const (
	// Job slice status : wait for running
	JSS_READY = 0

	// Job slice status : running
	JSS_RUNNING = 1

	// // Job slice status : success end
	JSS_COMPLETED = 2
)

type JobSlice struct {
	Id int64 `orm:"auto;pk"`

	Job *Job `orm:"rel(fk)"`

	// Slice Index
	Index int64

	// Slice status
	Status int

	ResultSetPath string
}

type Job struct {
	Id int64 `orm:"auto;pk"`

	// Job used data set
	UsedDataSet *DataSet `orm:"rel(fk)"`

	// Job used plugin id
	Plugin int64

	// Job split number
	SplitNumber int64

	// Job completed split block
	CompletedNumber int64

	// Job split slices
	Slices []*JobSlice `orm:"reverse(many)"`
}

var (
	ErrInvalidArgument     error = errors.New("invalid argument")
	ErrJobSliceIsCompleted error = errors.New("job slice completed")
	ErrJobSliceNotRunning  error = errors.New("job slice not running")
	ErrNoMoreData          error = errors.New("no more data")
)

func AddJob(dataSet *DataSet, plugin, splitNumber int64) (int64, error) {
	jobId, err := addJob(dataSet, plugin, splitNumber)
	if err != nil {
		return -1, err
	}

	jobSlices := make([]*JobSlice, splitNumber)
	for i := int64(0); i < splitNumber; i++ {
		id, err := addJobSlice(jobId, i)
		if err != nil {
			return -1, err
		}
		jobSlices[i] = &JobSlice{
			Id: id,
		}
	}

	err = updateJobSlices(jobId, jobSlices)
	if err != nil {
		return -1, err
	}

	return jobId, nil
}

func QueryJob(id int64) (d *Job, e error) {
	d = new(Job)

	o := orm.NewOrm()
	err := o.QueryTable(new(Job)).Filter("Id", id).RelatedSel().One(d)
	if err != nil {
		return nil, err
	}
	_, err = o.QueryTable(new(JobSlice)).Filter("Job", id).RelatedSel().All(&d.Slices)
	if err != nil {
		return nil, err
	}
	return d, nil
}

func QueryJobList() (ds []*Job, e error) {
	o := orm.NewOrm()

	_, err := o.QueryTable(new(Job)).RelatedSel().All(&ds)
	if err != nil {
		return nil, err
	}
	for _, d := range ds {
		_, err = o.QueryTable(new(JobSlice)).Filter("Job", d.Id).RelatedSel().All(&d.Slices)
		if err != nil {
			return nil, err
		}
	}
	return ds, nil
}

func addJob(dataSet *DataSet, plugin, splitNumber int64) (int64, error) {
	d := Job{
		UsedDataSet: dataSet,
		Plugin:      plugin,
		SplitNumber: splitNumber,
	}
	id, err := orm.NewOrm().Insert(&d)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func addJobSlice(jobId int64, index int64) (int64, error) {
	d := JobSlice{
		Job: &Job{
			Id: jobId,
		},
		Index:  index,
		Status: JSS_READY,
	}
	id, err := orm.NewOrm().Insert(&d)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func updateJobSlices(id int64, jobSlices []*JobSlice) error {
	d := Job{
		Id: id,
	}
	o := orm.NewOrm()
	err := o.Read(&d)
	if err != nil {
		return err
	}

	d.Slices = jobSlices

	_, err = o.Update(&d)
	if err != nil {
		return err
	}
	return nil
}

func ReadyJobSlice(id int64) error {
	d := JobSlice{
		Id: id,
	}
	o := orm.NewOrm()
	err := o.Read(&d)
	if err != nil {
		return err
	}

	if d.Status == JSS_COMPLETED {
		return ErrJobSliceIsCompleted
	}

	d.Status = JSS_READY

	_, err = o.Update(&d)
	if err != nil {
		return err
	}
	return nil
}

func RunningJobSlice(id int64) error {
	d := JobSlice{
		Id: id,
	}
	o := orm.NewOrm()
	err := o.Read(&d)
	if err != nil {
		return err
	}

	if d.Status == JSS_COMPLETED {
		return ErrJobSliceIsCompleted
	}

	d.Status = JSS_RUNNING

	_, err = o.Update(&d)
	if err != nil {
		return err
	}
	return nil
}

func CompletedJobSlice(id int64, resultSetPath string) error {
	d := JobSlice{
		Id:            id,
		ResultSetPath: resultSetPath,
	}
	o := orm.NewOrm()
	err := o.Read(&d)
	if err != nil {
		return err
	}

	if d.Status != JSS_RUNNING {
		return ErrJobSliceNotRunning
	}

	d.Job.CompletedNumber++

	d.Status = JSS_COMPLETED

	_, err = o.Update(&d)
	if err != nil {
		return err
	}
	_, err = o.Update(&d.Job)
	if err != nil {
		return err
	}
	return nil
}

func QueryReadyJobSlice() (ds []*JobSlice, e error) {
	o := orm.NewOrm()

	_, err := o.QueryTable(new(JobSlice)).Filter("Status", JSS_READY).RelatedSel().All(&ds)
	if err != nil {
		return nil, err
	}

	return ds, nil
}

func QueryRunningJobSlice() (ds []*JobSlice, e error) {
	o := orm.NewOrm()

	_, err := o.QueryTable(new(JobSlice)).Filter("Status", JSS_RUNNING).RelatedSel().All(&ds)
	if err != nil {
		return nil, err
	}

	return ds, nil
}

func QueryCompletedJobSlice() (ds []*JobSlice, e error) {
	o := orm.NewOrm()

	_, err := o.QueryTable(new(JobSlice)).Filter("Status", JSS_COMPLETED).RelatedSel().All(&ds)
	if err != nil {
		return nil, err
	}

	return ds, nil
}

func AcquireReadyJobSlice() (*JobSlice, error) {
	ds, err := QueryReadyJobSlice()
	if err != nil {
		return nil, err
	}

	if len(ds) == 0 {
		return nil, ErrNoMoreData
	}

	err = RunningJobSlice(ds[0].Id)
	if err != nil {
		return nil, err
	}

	return ds[0], nil
}
