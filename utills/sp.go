package utills

import (
	"bytes"
)

func JoinStrings(arr []string) string {
	var buffer bytes.Buffer
	for index := 0; index < len(arr); index++ {
		buffer.WriteString(arr[index])
	}
	ns := buffer.String()
	return ns
}
