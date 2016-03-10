// init
package models

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/mattn/go-sqlite3"
)

func init() {
	orm.RegisterDataBase("default", "sqlite3", "../store/db.sqlite3")
	orm.RegisterModel(
		new(DataSet),
		new(ResultSet),
		new(Job),
		new(JobSlice),
	)
}

func Install() error {
	err := orm.RunSyncdb("default", true, true)
	if err != nil {
		return err
	}
	return nil
}
