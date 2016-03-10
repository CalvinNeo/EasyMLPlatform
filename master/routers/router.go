// @APIVersion 0.0.1
// @Title Mokou Machine Learning Base Platform API
// @Description support base functions for Mokou Machine Learning Platform
// @Contact liuhanlcj1994@gmail.com
// @TermsOfServiceUrl http://reficuls.cn/
// @License Apache 2.0
// @LicenseUrl http://www.apache.org/licenses/LICENSE-2.0.html
package routers

import (
	"mlp/master/controllers"

	"github.com/astaxie/beego/context"

	"github.com/astaxie/beego"
)

func init() {
	filterAccess := func(ctx *context.Context) {
		ctx.Output.Header("Access-Control-Allow-Origin", "*")
	}

	beego.InsertFilter("/swagger", beego.BeforeExec, filterAccess, true)

	ns := beego.NewNamespace("/v1",
		beego.NSNamespace("/data_set",
			beego.NSInclude(
				&controllers.DataSetController{},
			),
		),
		beego.NSNamespace("/job",
			beego.NSInclude(
				&controllers.JobController{},
			),
		),
		beego.NSNamespace("/node",
			beego.NSInclude(
				&controllers.NodeController{},
			),
		),
		beego.NSNamespace("/job_slice",
			beego.NSInclude(
				&controllers.JobSliceController{},
			),
		),
		beego.NSNamespace("/result_set",
			beego.NSInclude(
				&controllers.ResultSetController{},
			),
		),
	)

	beego.AddNamespace(ns)

}
