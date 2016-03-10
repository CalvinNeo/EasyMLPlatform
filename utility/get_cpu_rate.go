// get_cpu_rate
package utility

import (
	"syscall"
	"time"
	"unsafe"
)

type FILETIME struct {
	LowDateTime  uint32
	HighDateTime uint32
}

var (
	kernel32 *syscall.LazyDLL

	getSystemTimes *syscall.LazyProc
)

func init() {
	kernel32 = syscall.NewLazyDLL("kernel32.dll")

	getSystemTimes = kernel32.NewProc("GetSystemTimes")
}

func FileTimeToDouble(ft FILETIME) float64 {
	return float64(ft.HighDateTime)*4.294967296E9 + float64(ft.LowDateTime)
}

func GetSystemTimes(ftIdel, ftKernel, ftUser *FILETIME) error {
	r1, _, e1 := syscall.Syscall(getSystemTimes.Addr(), 3, uintptr(unsafe.Pointer(ftIdel)), uintptr(unsafe.Pointer(ftKernel)), uintptr(unsafe.Pointer(ftUser)))
	if r1 == 0 {
		if e1 != 0 {
			return error(e1)
		} else {
			return syscall.EINVAL
		}
	}
	return nil
}

func GetCpuUsedRate() (float64, error) {
	var (
		ftIdel1, ftIdel2     FILETIME
		ftKernel1, ftKernel2 FILETIME
		ftUser1, ftUser2     FILETIME
	)

	err := GetSystemTimes(&ftIdel1, &ftKernel1, &ftUser1)
	if err != nil {
		return 0, err
	}

	time.Sleep(time.Millisecond * 1000)

	err = GetSystemTimes(&ftIdel2, &ftKernel2, &ftUser2)
	if err != nil {
		return 0, err
	}

	ivIdel := FileTimeToDouble(ftIdel2) - FileTimeToDouble(ftIdel1)
	ivKernel := FileTimeToDouble(ftKernel2) - FileTimeToDouble(ftKernel1)
	ivUser := FileTimeToDouble(ftUser2) - FileTimeToDouble(ftUser1)

	return (1 - ivIdel/(ivUser+ivKernel)) * 100, nil
}
