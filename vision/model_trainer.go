/*
 * model_trainer.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Fri Feb 08 2019 9:52:09 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

package vision

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/ATOM/database"
	"github.com/ATOM/utills"
	"gocv.io/x/gocv"
	"gocv.io/x/gocv/contrib"
)

type ModelTrainer struct {
	sbm *database.SQLiteManager
}

func NewModelTrainer() *ModelTrainer {
	mt := ModelTrainer{}
	mt.sbm = database.NewSQLiteManager()
	return &mt
}

func (m *ModelTrainer) trainModel() {
	var images []gocv.Mat
	var labels []string
	classifier := NewClassifier()
	peoplesDir := utills.PeoplesImagesDir()

	filepath.Walk(peoplesDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			fmt.Printf("prevent panic by handling failure accessing a path %q: %v\n", path, err)
			return err
		}
		if !info.IsDir() {
			img := gocv.IMRead(path, 0)
			face := classifier.faceFromImage(img)
			if face != nil {
				dir := filepath.Dir(path)
				parent := filepath.Base(dir)
				labels = append(labels, parent)
				images = append(images, *face)
			}
		}
		return nil
	})

	if len(images) == 0 {
		return
	}

	labelIds := m.labelIdsForImages(images, labels)
	recognizer := contrib.NewLBPHFaceRecognizer()
	modelPath := utills.ModelPath()
	if _, err := os.Stat(modelPath); os.IsNotExist(err) {
		recognizer.Train(images, labelIds)
	} else {
		recognizer.LoadFile(modelPath)
		recognizer.Update(images, labelIds)
	}
	recognizer.SaveFile(modelPath)
	err = utills.RemoveContents(peoplesDir)
	if err != nil {
		fmt.Println("Delete training images: ", err)
	}
}

func (m *ModelTrainer) labelIdsForImages(images []gocv.Mat, labels []string) (labelIDs []int) {

	unique := utills.RemoveDuplicateStrings(labels)

	labelMap := make(map[string]int)

	for _, element := range unique {
		sm := database.NewSQLiteManager()
		d, err := sm.IdForLabel(element)
		if err != nil {
			fmt.Println(err.Error())
		}
		labelMap[element] = int(*d)
	}

	var labelIds []int

	for _, element := range labels {
		labelIds = append(labelIds, labelMap[element])
	}
	return labelIds
}
