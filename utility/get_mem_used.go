// get_mem_used
package utility

import (
	"fmt"
	"os/exec"
	"strings"
)
import "code.google.com/p/mahonia"

func GetUsedPhysicalMemory() (int64, error) {
	t, err := GetTotalPhysicalMemory()
	if err != nil {
		return -1, err
	}

	f, err := GetFreePhysicalMemory()
	if err != nil {
		return -1, err
	}

	return t - f, nil
}

func GetFreePhysicalMemory() (int64, error) {
	d, err := exec.Command("cmd", "/c", "wmic OS get FreePhysicalMemory").Output()
	if err != nil {
		return -1, err
	}

	dec := mahonia.NewDecoder("GBK")

	s := dec.ConvertString(string(d))

	r := strings.NewReader(s)

	var tmp string
	var n int64
	fmt.Fscanln(r, &tmp)
	fmt.Fscanln(r, &n)

	return n, nil
}

func GetTotalPhysicalMemory() (int64, error) {
	d, err := exec.Command("cmd", "/c", "wmic memphysical get MaxCapacity").Output()
	if err != nil {
		return -1, err
	}

	dec := mahonia.NewDecoder("GBK")

	s := dec.ConvertString(string(d))

	r := strings.NewReader(s)

	var tmp string
	var n int64
	fmt.Fscanln(r, &tmp)
	fmt.Fscanln(r, &n)

	return n, nil
}
