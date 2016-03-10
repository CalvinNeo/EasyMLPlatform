// copy_file
package utility

import (
	"io"
	"os"
)

func CopyFile(src, des string) (w int64, err error) {
	srcFile, err := os.OpenFile(src, os.O_RDONLY, 0)
	if err != nil {
		return -1, err
	}
	defer srcFile.Close()

	desFile, err := os.Create(des)
	if err != nil {
		return -1, err
	}
	defer desFile.Close()

	return io.Copy(desFile, srcFile)
}

func CopyFile2(src io.Reader, des string) (w int64, err error) {
	desFile, err := os.Create(des)
	if err != nil {
		return -1, err
	}
	defer desFile.Close()

	return io.Copy(desFile, src)
}
