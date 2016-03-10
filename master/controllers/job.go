// job
package controllers

import (
	"log"
	"mlp/master/models"
	"strconv"

	"github.com/astaxie/beego"
)

// Job API Controller
type JobController struct {
	beego.Controller
}

// @Title Submit
// @Description Submit a new job
// @Param	dataSetId	form 	int64	true		"The job used data set id"
// @Param	pluginId	form 	int64	true		"The job used plugin id"
// @Param	splitNumber	form 	int64	true		"Job split number"
// @Success 200 {string} the job id
// @Failure 403 {string} error description
// @router /submit [post]
func (o *JobController) Submit() {
	dataSetId, err := o.GetInt64("dataSetId")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	pluginId, err := o.GetInt64("pluginId")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	splitNumber, err := o.GetInt64("splitNumber")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	d, err := models.QueryDataSet(dataSetId)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	if pluginId != 1 {
		FinishRequest(o.Ctx, 403, "unknow plugin id")
		return
	}

	if splitNumber <= 0 {
		FinishRequest(o.Ctx, 403, "invalid cut number")
		return
	}

	id, err := models.AddJob(d, pluginId, splitNumber)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	o.Ctx.WriteString(strconv.Itoa(int(id)))
}

type Job struct {
	Id int64

	// Job used data set
	UsedDataSet DataSet

	// Job used plugin id
	Plugin int64

	// Job split number
	SplitNumber int64

	// Job completed split block
	CompletedNumber int64

	// Job split slices
	Slices []*models.JobSlice
}

type JobList struct {
	Objects []Job
}

func newJob(d *models.Job) Job {
	return Job{
		Id:              d.Id,
		UsedDataSet:     newDataSet(d.UsedDataSet),
		Plugin:          d.Plugin,
		SplitNumber:     d.SplitNumber,
		CompletedNumber: d.CompletedNumber,
		Slices:          d.Slices,
	}
}

// @Title Query List
// @Description Query all job info
// @Success 200 {object} controllers.JobList
// @Failure 403 {string} error description
// @router /query/list [post]
func (o *JobController) QueryList() {
	ds, err := models.QueryJobList()
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
	vds := make([]Job, len(ds))
	for i, d := range ds {
		vds[i] = newJob(d)
	}
	o.Data["json"] = JobList{
		Objects: vds,
	}
	o.ServeJson()
}

// @Title Query
// @Description Query job info
// @Param	id	form 	int64	true		"Job id"
// @Success 200 {object} controllers.Job
// @Failure 403 {string} error description
// @router /query [post]
func (o *JobController) Query() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	d, err := models.QueryJob(id)
	if err != nil {
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
	o.Data["json"] = newJob(d)
	o.ServeJson()
}
