// data_set
package models

import "github.com/astaxie/beego/orm"

type DataSet struct {
	Id int64 `orm:"auto;pk"`

	FilePath string

	// Meta data
	Meta string

	// Ext data
	Ext string

	// Data line number
	LineNumber int64

	// Data set if has header
	DropHeader bool
}

func AddDataSet(filePath string, lineNumber int64, dropHeader bool) (int64, error) {
	d := DataSet{
		FilePath:   filePath,
		LineNumber: lineNumber,
		DropHeader: dropHeader,
	}
	id, err := orm.NewOrm().Insert(&d)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func UpdateDataSet(id int64, meta, ext string) error {
	d := DataSet{
		Id: id,
	}
	o := orm.NewOrm()
	err := o.Read(&d)
	if err != nil {
		return err
	}
	if len(meta) > 0 {
		d.Meta = meta
	}
	if len(ext) > 0 {
		d.Ext = ext
	}
	_, err = o.Update(&d)
	if err != nil {
		return err
	}
	return nil
}

func QueryDataSet(id int64) (*DataSet, error) {
	d := DataSet{
		Id: id,
	}
	err := orm.NewOrm().Read(&d)
	if err != nil {
		return nil, err
	}
	return &d, nil
}

func QueryDataSetList() ([]*DataSet, error) {
	ds := []*DataSet{}
	_, err := orm.NewOrm().QueryTable("DataSet").All(&ds)
	if err != nil {
		return nil, err
	}
	return ds, nil
}

func DeleteDataSet(id int64) error {
	d := DataSet{
		Id: id,
	}
	_, err := orm.NewOrm().Delete(&d)
	if err != nil {
		return err
	}
	return nil
}
