// main
package main

import (
	"log"
	"mlp/node/api"
	"mlp/utility"
	"time"

	"github.com/astaxie/beego/config"
)

const (
	acquireJobSleepTime = 8
)

var (
	mapi *api.MasterApi
	cfg  config.ConfigContainer
)

func init() {
	log.SetFlags(log.Lshortfile | log.LstdFlags)

	var err error

	cfg, err = config.NewConfig("ini", "config.ini")
	if err != nil {
		log.Fatalln(err)
	}

	hostname := cfg.String("hostname")

	mapi = api.New(hostname)
}

func main() {
	id, err := mapi.AcquireId()
	if err != nil {
		log.Fatalln(err)
	}

	log.Println("Node ID :", id)

	go Aliver(id)

	for {
		can, err := CheckCanNewWork()
		if err != nil {
			log.Println(err)
			time.Sleep(time.Second * acquireJobSleepTime)
			continue
		}

		if can {
			js, err := mapi.AcquireJobSlice()
			if err != nil {
				if err != api.ErrNoMoreData {
					log.Println(err)
				}
				time.Sleep(time.Second * acquireJobSleepTime)
				continue
			}

			go NewWork(js)
		}

		time.Sleep(time.Second * acquireJobSleepTime)
	}
}

func CheckCanNewWork() (bool, error) {
	freeMemory, err := utility.GetFreePhysicalMemory()
	if err != nil {
		return false, err
	}

	cpuUsed, err := utility.GetCpuUsedRate()
	if err != nil {
		return false, err
	}

	log.Println("Free Memory :", freeMemory, "CPU :", cpuUsed)

	if freeMemory <= 1024*512 {
		return false, nil
	}

	if cpuUsed >= 90 {
		return false, nil
	}

	return true, nil
}
