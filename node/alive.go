// alive
package main

import (
	"log"
	"mlp/utility"
	"time"
)

const (
	aliveSleepTime = 5
)

func Aliver(id int64) {
	for {
		freeMemory, err := utility.GetFreePhysicalMemory()
		if err != nil {
			time.Sleep(time.Second * aliveSleepTime)
			continue
		}

		cpuUsed, err := utility.GetCpuUsedRate()
		if err != nil {
			time.Sleep(time.Second * aliveSleepTime)
			continue
		}

		err = mapi.Alive(id, cpuUsed, float64(freeMemory))
		if err != nil {
			log.Println("Report alive failed :", err)
		}

		time.Sleep(time.Second * aliveSleepTime)
	}
}
