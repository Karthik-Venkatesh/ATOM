package constants

import (
	"bytes"
	"path"
	"runtime"
)

func TrainningImagesDir() string {
	var buffer bytes.Buffer
	buffer.WriteString(ProjectFolder())
	buffer.WriteString("/data/training_images")
	newFileName := buffer.String()
	return newFileName
}

func ProjectFolder() string {
	_, filename, _, _ := runtime.Caller(1)
	var buffer bytes.Buffer
	buffer.WriteString(path.Dir(filename))
	buffer.WriteString("/..")
	projectPath := path.Clean(buffer.String())
	return projectPath
}
