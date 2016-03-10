// data_set
package controllers

import (
	"log"
	"mlp/master/models"
	"mlp/utility"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/astaxie/beego"
)

// DataSet API Controller
type DataSetController struct {
	beego.Controller
}

// @Title Upload
// @Description Upload a new data set to server by file path
// @Param	filePath	form 	string	true		"The data set file path, must as same server"
// @Param	dropHeader	form 	bool	true		"The data set if has header"
// @Success 200 {string} the data set id
// @Failure 403 {string} error description
// @router /upload/path [post]
func (o *DataSetController) UploadByPath() {
	filePath := o.GetString("filePath")

	dropHeader, err := o.GetBool("dropHeader")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	filename := utility.AcquireFilename()
	_, err = utility.CopyFile(filePath, "../store/"+filename)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	lineNumber, err := utility.GetFileLineNumber("../store/" + filename)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	id, err := models.AddDataSet(filename, lineNumber, dropHeader)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	o.Ctx.WriteString(strconv.Itoa(int(id)))
}

// @Title Set
// @Description Set meta data and ext data. If the param is empty string, then the original ext data are retained
// @Param	id		form 	int64	true		"The data set id"
// @Param	meta	form 	string	true		"The data set's meta data"
// @Param	ext		form 	string	true		"The data set's ext data"
// @Success 200 body is empty
// @Failure 403 {string} error description
// @router /set [post]
func (o *DataSetController) Set() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	meta := o.GetString("meta")
	ext := o.GetString("ext")

	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	err = models.UpdateDataSet(id, meta, ext)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
}

// @Title Delete
// @Description Delete data set
// @Param	id		form 	int64	true		"The data set id"
// @Success 200 body is empty
// @Failure 403 {string} error description
// @router /delete [post]
func (o *DataSetController) Delete() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	err = models.DeleteDataSet(id)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
}

type DataSet struct {
	Id int64

	// Meta data
	Meta string

	// Ext data
	Ext string

	// Data line number
	LineNumber int64
}

type DataSetList struct {
	Objects []DataSet
}

func newDataSet(d *models.DataSet) DataSet {
	return DataSet{
		Id:         d.Id,
		Meta:       d.Meta,
		Ext:        d.Ext,
		LineNumber: d.LineNumber,
	}
}

// @Title Query
// @Description Query data set info
// @Param	id		form 	int64	true		"The data set id"
// @Success 200 {object} controllers.DataSet
// @Failure 403 {string} error description
// @router /query [post]
func (o *DataSetController) Query() {
	id, err := o.GetInt64("id")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	d, err := models.QueryDataSet(id)
	if err != nil {
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
	o.Data["json"] = newDataSet(d)
	o.ServeJson()
}

// @Title Query List
// @Description Query all data set info
// @Success 200 {object} controllers.DataSetList
// @Failure 403 {string} error description
// @router /query/list [post]
func (o *DataSetController) QueryList() {
	ds, err := models.QueryDataSetList()
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
	vds := make([]DataSet, len(ds))
	for i, d := range ds {
		vds[i] = newDataSet(d)
	}
	o.Data["json"] = DataSetList{
		Objects: vds,
	}
	o.ServeJson()
}

// @Title Download
// @Description Down data set
// @Param	id				query 	int64	true		"The data set id"
// @Param	splitNumber		query 	int64	true		"Data set split number"
// @Param	index			query 	int64	true		"Data set split index"
// @Success 200 {[]byte} data set
// @Failure 403 {string} error description
// @router /download [get]
func (o *DataSetController) DownloadDataSetSlice() {
	id, err := o.GetInt64("id")
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

	index, err := o.GetInt64("index")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	d, err := models.QueryDataSet(id)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	perSplitLineNumber := d.LineNumber
	if d.DropHeader {
		perSplitLineNumber--
	}

	perSplitLineNumber = perSplitLineNumber / splitNumber

	startLineNumber := index * perSplitLineNumber

	dataSetSliceBytes, err := utility.GetFilePointLineData("../store/"+d.FilePath, startLineNumber, perSplitLineNumber)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	filename := strings.TrimSuffix(d.FilePath, filepath.Ext(d.FilePath))

	o.Ctx.Output.Header("Content-Description", "File Transfer")
	o.Ctx.Output.Header("Content-Type", "application/octet-stream")
	o.Ctx.Output.Header("Content-Disposition", "attachment; filename="+filename+"-"+strconv.Itoa(int(index))+".d")
	o.Ctx.Output.Header("Content-Transfer-Encoding", "binary")
	o.Ctx.Output.Header("Expires", "0")
	o.Ctx.Output.Header("Cache-Control", "must-revalidate")
	o.Ctx.Output.Header("Pragma", "public")
	o.Ctx.Output.Body(dataSetSliceBytes)
}
