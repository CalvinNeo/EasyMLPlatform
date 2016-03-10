// result_set
package controllers

import (
	"log"
	"mlp/master/models"
	"mlp/utility"

	"github.com/astaxie/beego"
)

// ResultSet API Controller
type ResultSetController struct {
	beego.Controller
}

// @Title Upload
// @Description Upload result set
// @Param	file		form 	file	true		"Result set data"
// @Param	jobSliceId	form 	int64	true		"The job slice id"
// @Success 200 body is empty
// @Failure 403 {string} error description
// @router /upload [post]
func (o *ResultSetController) Upload() {
	f, _, err := o.GetFile("file")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
	defer f.Close()

	//	fileSize, err := o.GetInt64("fileSize")
	//	if err != nil {
	//		log.Println(err)
	//		FinishRequest(o.Ctx, 403, err.Error())
	//		return
	//	}

	jobSliceId, err := o.GetInt64("jobSliceId")
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	filename := utility.AcquireFilename()
	_, err = utility.CopyFile2(f, "../store/"+filename)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}

	err = models.CompletedJobSlice(jobSliceId, filename)
	if err != nil {
		log.Println(err)
		FinishRequest(o.Ctx, 403, err.Error())
		return
	}
}
