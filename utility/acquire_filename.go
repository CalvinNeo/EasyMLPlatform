// acquire_filename
package utility

import (
	"strconv"
	"time"
)

func AcquireFilename() string {
	namePrefix := strconv.FormatInt(int64(time.Now().Unix()), 10) + "-"
	i := 0
	for {
		filename := namePrefix + strconv.Itoa(i) + ".d"
		if FileExist("../store/" + filename) {
			i++
			continue
		}
		return filename
	}
	return ""
}
