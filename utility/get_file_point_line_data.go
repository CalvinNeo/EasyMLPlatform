// get_file_point_line_data
package utility

import (
	"bufio"
	"io"
	"os"
)

func GetFilePointLineData(filename string, startLineNumber, count int64) ([]byte, error) {
	r, err := os.OpenFile(filename, os.O_RDONLY, 0)
	if err != nil {
		return nil, err
	}
	defer r.Close()

	br := bufio.NewReader(r)

	for i := int64(0); i < startLineNumber; i++ {
		_, err := br.ReadBytes('\n')
		if err != nil {
			return nil, err
		}
	}

	data := []byte{}

	for i := int64(0); i < count; i++ {
		ld, err := br.ReadBytes('\n')
		if err != nil {
			if err == io.EOF {
				data = append(data, ld...)
				return data, nil
			}
			return nil, err
		}
		data = append(data, ld...)
	}

	return data, nil
}
