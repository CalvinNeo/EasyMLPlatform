// master_api
package api

import (
	"encoding/json"
	"errors"
	"fmt"
	"io/ioutil"
	"mlp/master/models"
	"strconv"
	"strings"

	"github.com/astaxie/beego/httplib"
)

type MasterApi struct {
	Hostname string
}

var (
	ErrNoMoreData error = errors.New("no more data")
	ErrApiFailed  error = errors.New("remote api call failed")
)

func New(hostname string) *MasterApi {
	if strings.HasPrefix(hostname, "http://") {
		hostname = strings.TrimPrefix(hostname, "http://")
	}

	if strings.HasSuffix(hostname, "/") {
		hostname = strings.TrimSuffix(hostname, "/")
	}

	return &MasterApi{
		Hostname: hostname,
	}
}

func (m MasterApi) AcquireId() (int64, error) {
	req := httplib.Post(fmt.Sprintf("http://%s/v1/node/acquire", m.Hostname))

	resp, err := req.Response()
	if err != nil {
		return -1, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return -1, ErrApiFailed
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return -1, err
	}

	id, err := strconv.ParseInt(string(body), 10, 64)
	if err != nil {
		return -1, err
	}

	return id, nil
}

func (m MasterApi) Alive(id int64, cpu, memory float64) error {
	req := httplib.Post(fmt.Sprintf("http://%s/v1/node/alive", m.Hostname))

	req = req.Param("id", strconv.FormatInt(id, 10))
	req = req.Param("cpu", strconv.FormatFloat(cpu, 'f', 2, 64))
	req = req.Param("memory", strconv.FormatFloat(memory, 'f', 2, 64))

	resp, err := req.Response()
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return ErrApiFailed
	}

	return nil
}

func (m MasterApi) DownloadDataSetSplit(id, splitNumber, index int64) (string, error) {
	req := httplib.Post(fmt.Sprintf("http://%s/v1/data_set/download", m.Hostname))

	req = req.Param("id", strconv.FormatInt(id, 10))
	req = req.Param("splitNumber", strconv.FormatInt(splitNumber, 10))
	req = req.Param("index", strconv.FormatInt(index, 10))

	resp, err := req.Response()
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return "", ErrApiFailed
	}

	filename := strings.TrimPrefix(resp.Header.Get("Content-Disposition"), "attachment; filename=")

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	err = ioutil.WriteFile("../tmp/"+filename, body, 0)
	if err != nil {
		return "", err
	}

	return filename, nil
}

func (m MasterApi) AcquireJobSlice() (*models.JobSlice, error) {
	req := httplib.Post(fmt.Sprintf("http://%s/v1/job_slice/acquire", m.Hostname))

	resp, err := req.Response()
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		if resp.StatusCode == 204 {
			return nil, ErrNoMoreData
		} else {
			return nil, ErrApiFailed
		}
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	js := models.JobSlice{}
	err = json.Unmarshal(body, &js)
	if err != nil {
		return nil, err
	}

	return &js, nil
}

func (m MasterApi) UploadResultSetSlice(id int64, filePath string) error {
	req := httplib.Post(fmt.Sprintf("http://%s/v1/job_slice/acquire", m.Hostname))

	req = req.PostFile("file", filePath)

	resp, err := req.Response()
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return ErrApiFailed
	}

	return nil
}
