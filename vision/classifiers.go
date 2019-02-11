/*
 * classifiers.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Sat Feb 09 2019 9:07:34 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */
package vision

import (
	"fmt"
	"image"
	"path"

	"github.com/ATOM/utills"
	"gocv.io/x/gocv"
)

type Classifier struct {
	FrontalFace gocv.CascadeClassifier
}

func NewClassifier() *Classifier {
	c := Classifier{}
	c.loadFrontalFaceClassifier()
	return &c
}

func (c *Classifier) loadFrontalFaceClassifier() {
	// load classifier to recognize faces
	c.FrontalFace = gocv.NewCascadeClassifier()
	cascadePath := path.Join(utills.HaarCascadesDir(), "haarcascade_frontalface_alt2.xml")
	success := c.FrontalFace.Load(cascadePath)
	if !success {
		fmt.Println("Error: haarcascade_frontalface_alt2 laoding xml")
	}
}

func (c *Classifier) faceFromImage(img gocv.Mat) *gocv.Mat {
	// detect faces

	rects := c.FrontalFace.DetectMultiScaleWithParams(img, 1.1, 5, 0, image.Point{X: 100, Y: 100}, image.Point{X: 500, Y: 500})
	fmt.Println("Classifier - number of faces found : ", len(rects))
	for _, r := range rects {
		face := img.Region(r)
		return &face
	}
	fmt.Println("Classifier: Face not found")
	return nil
}
