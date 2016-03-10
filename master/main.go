package main

import (
	"log"
	_ "mlp/master/docs"
	"mlp/master/models"
	_ "mlp/master/routers"
	"os"

	"github.com/astaxie/beego"
)

func init() {
	log.SetFlags(log.Lshortfile | log.LstdFlags)
}

func main() {
	if len(os.Args) > 1 {
		switch len(os.Args) {
		case 2:
			if os.Args[1] == "init" {
				models.Install()
			}
		}
		return
	}

	docSwitch, err := beego.AppConfig.Bool("EnableDocs")
	if err != nil {
		log.Fatalln(err)
	}

	if docSwitch {
		beego.DirectoryIndex = true
		beego.StaticDir["/swagger"] = "swagger"
	}

	monitorSwitch, err := beego.AppConfig.Bool("EnableMonitor")
	if err != nil {
		log.Fatalln(err)
	}

	if monitorSwitch {
		beego.StaticDir["/inspinia"] = "inspinia"
	}

	beego.Run()
}
