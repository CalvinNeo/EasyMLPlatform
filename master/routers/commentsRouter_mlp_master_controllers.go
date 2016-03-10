package routers

import (
	"github.com/astaxie/beego"
)

func init() {

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"UploadByPath",
			`/upload/path`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"Set",
			`/set`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"Delete",
			`/delete`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"Query",
			`/query`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"QueryList",
			`/query/list`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:DataSetController"],
		beego.ControllerComments{
			"DownloadDataSetSlice",
			`/download`,
			[]string{"get"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:JobController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:JobController"],
		beego.ControllerComments{
			"Submit",
			`/submit`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:JobController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:JobController"],
		beego.ControllerComments{
			"QueryList",
			`/query/list`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:JobController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:JobController"],
		beego.ControllerComments{
			"Query",
			`/query`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:JobSliceController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:JobSliceController"],
		beego.ControllerComments{
			"AcquireJobSlice",
			`/acquire`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:NodeController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:NodeController"],
		beego.ControllerComments{
			"Acquire",
			`/acquire`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:NodeController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:NodeController"],
		beego.ControllerComments{
			"Alive",
			`/alive`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:NodeController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:NodeController"],
		beego.ControllerComments{
			"Query",
			`/query`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:NodeController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:NodeController"],
		beego.ControllerComments{
			"QueryList",
			`/query/list`,
			[]string{"post"},
			nil})

	beego.GlobalControllerRouter["mlp/master/controllers:ResultSetController"] = append(beego.GlobalControllerRouter["mlp/master/controllers:ResultSetController"],
		beego.ControllerComments{
			"Upload",
			`/upload`,
			[]string{"post"},
			nil})

}
