// work
package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"mlp/master/models"
	"os/exec"
)

func NewWork(js *models.JobSlice) {
	filename, err := mapi.DownloadDataSetSplit(js.Job.UsedDataSet.Id, js.Job.SplitNumber, js.Index)
	if err != nil {
		log.Println(err)
		return
	}

	startParam := map[string]string{
		"FilePath": filename,
		"Ext":      js.Job.UsedDataSet.Ext,
		"Meta":     js.Job.UsedDataSet.Meta,
	}

	jd, err := json.Marshal(startParam)
	if err != nil {
		log.Println(err)
		return
	}

	err = ioutil.WriteFile("../tmp/"+filename+".json", jd, 0)
	if err != nil {
		log.Println(err)
		return
	}

	od, err := exec.Command("python.exe", "../py/plugin1.py", filename+".json").Output()
	if err != nil {
		log.Println(err)
		return
	}

	outputJson := map[string]string{}

	err = json.Unmarshal(od, outputJson)
	if err != nil {
		log.Println(err)
		return
	}

	resultSetPath, ok := outputJson["resultSetFilePath"]
	if !ok {
		log.Println("can not find result file path key")
		return
	}

	err = mapi.UploadResultSetSlice(js.Id, "../py/"+resultSetPath)
	if !ok {
		log.Println("can not upload result :", err)
		return
	}
}
