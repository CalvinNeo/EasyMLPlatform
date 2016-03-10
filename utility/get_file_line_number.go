// get_file_line_number
package utility

import (
	"bufio"
	"errors"
	"io"
	"os"
)

func GetFileLineNumber(filename string) (int64, error) {
	r, err := os.OpenFile(filename, os.O_RDONLY, 0)
	if err != nil {
		return -1, err
	}
	defer r.Close()

	br := bufio.NewReader(r)

	lineNumber := int64(0)

	for {
		_, err := br.ReadBytes('\n')
		if err != nil {
			if err == io.EOF {
				lineNumber++
				return lineNumber, nil
			}
			return -1, err
		}
		lineNumber++
	}

	return -1, errors.New("unknow")
}
