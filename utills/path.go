/*
 * path.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Fri Feb 08 2019 9:51:44 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

package utills

import (
	"fmt"
	"os"
	"path"
	"path/filepath"
	"runtime"
)

func TrainningImagesDir() string {
	pathComponents := []string{ProjectFolder(), "/data/training_images"}
	path := JoinStrings(pathComponents)
	return path
}

func ProjectFolder() string {
	_, filename, _, _ := runtime.Caller(1)
	pathComponents := []string{path.Dir(filename), "/.."}
	projectPath := JoinStrings(pathComponents)
	projectPath = path.Clean(projectPath)
	return projectPath
}

func VisionDir() string {
	pathComponents := []string{ProjectFolder(), "/vision/"}
	path := JoinStrings(pathComponents)
	dir := filepath.Dir(path)
	return dir
}

func HaarCascadesDir() string {
	pathComponents := []string{ProjectFolder(), "/vision/cascades/data/haarcascades/"}
	path := JoinStrings(pathComponents)
	dir := filepath.Dir(path)
	return dir
}

func LabeledDir(label string) string {
	pathComponents := []string{TrainningImagesDir(), "/", label}
	path := JoinStrings(pathComponents)
	return path
}

func ModelPath() string {
	pathComponents := []string{ProjectFolder(), "/data//model/", "vision.yaml"}
	path := JoinStrings(pathComponents)
	dir := filepath.Dir(path)
	createDirIfNotExists(dir)
	return path
}

func DatabasePath() string {
	pathComponents := []string{ProjectFolder(), "/data/database/", "model.db"}
	path := JoinStrings(pathComponents)
	dir := filepath.Dir(path)
	createDirIfNotExists(dir)
	return path
}

func createDirIfNotExists(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.MkdirAll(path, os.ModePerm)
		if err != nil {
			fmt.Println(err.Error())
		}
	}
}
