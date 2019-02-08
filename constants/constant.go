package constants

import (
	"path"
	"runtime"

	"github.com/ATOM/utills"
)

func TrainningImagesDir() string {
	pathComponents := []string{ProjectFolder(), "/data/training_images"}
	path := utills.JoinStrings(pathComponents)
	return path
}

func ProjectFolder() string {
	_, filename, _, _ := runtime.Caller(1)
	pathComponents := []string{path.Dir(filename), "/.."}
	projectPath := utills.JoinStrings(pathComponents)
	projectPath = path.Clean(projectPath)
	return projectPath
}
