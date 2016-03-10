// job_slice
package controllers

import (
	"mlp/master/models"

	"github.com/astaxie/beego"
)

// Job slice API Controller
type JobSliceController struct {
	beego.Controller
}

// @Title Acquire Job Slice
// @Description Acquire a job slice that status is ready to work
// @Success 200 {object} models.JobSlice
// @Failure 403 {string} error description
// @router /acquire [post]
func (o *JobSliceController) AcquireJobSlice() {
	//	id, err := o.GetInt64("id")
	//	if err != nil {
	//		log.Println(err)
	//		FinishRequest(o.Ctx, 403, err.Error())
	//		return
	//	}

	d, err := models.AcquireReadyJobSlice()
	if err != nil {
		if err == models.ErrNoMoreData {
			FinishRequest(o.Ctx, 204, "")
		} else {
			FinishRequest(o.Ctx, 403, err.Error())
		}
		return
	}

	o.Data["json"] = d
	o.ServeJson()
}
