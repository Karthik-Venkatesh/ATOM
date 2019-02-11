/*
 * vision.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Mon Feb 04 2019 9:26:36 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

package vision

import (
	"fmt"
	"image"
	"image/color"
	"io/ioutil"
	"os"
	"strconv"

	"github.com/ATOM/utills"
	"gocv.io/x/gocv"
)

type Vision struct {
	videoCapture *gocv.VideoCapture
	window       *gocv.Window
	Classifier   *Classifier
}

func NewVision() *Vision {
	v := Vision{}
	v.Classifier = NewClassifier()
	return &v
}

func (v *Vision) StartVision() {

	if v.videoCapture == nil {
		webcam, _ := gocv.VideoCaptureDevice(0)
		defer webcam.Close()
		v.videoCapture = webcam
	}

	v.window = gocv.NewWindow("atom-vision")

	img := gocv.NewMat()
	defer img.Close()

	// load classifier to recognize faces
	classifier := v.Classifier
	if classifier == nil {
		fmt.Printf("Error: haarcascade_frontalface_alt2 laoding xml")
	}

	for {
		if ok := v.videoCapture.Read(&img); !ok {
			return
		}
		if img.Empty() {
			continue
		}

		// detect faces
		rects := classifier.FrontalFace.DetectMultiScaleWithParams(img, 1.1, 5, 0, image.Point{X: 100, Y: 100}, image.Point{X: 500, Y: 500})
		fmt.Printf("found %d faces\n", len(rects))

		if len(rects) > 0 {
			v.saveFacesImage(img)
		}

		v.drawRect(rects, img)

		// show the image in the window, and wait 1 millisecond
		v.window.IMShow(img)
		if v.window.WaitKey(1) >= 0 {
			break
		}
	}
}

func (v *Vision) StopVision() {
	v.videoCapture.Close()
}

func (v *Vision) drawRect(rects []image.Rectangle, img gocv.Mat) {
	// color for the rect when faces detected
	blue := color.RGBA{0, 0, 255, 0}

	// draw a rectangle around each face on the original image,
	// along with text identifying as "Human"
	for _, r := range rects {
		gocv.Rectangle(&img, r, blue, 3)

		size := gocv.GetTextSize("Human", gocv.FontHersheyPlain, 1.2, 2)
		pt := image.Pt(r.Min.X+(r.Min.X/2)-(size.X/2), r.Min.Y-2)
		gocv.PutText(&img, "Human", pt, gocv.FontHersheyPlain, 1.2, blue, 2)
	}
}

func (v *Vision) saveFacesImage(img gocv.Mat) {

	trainningImagesDir := utills.LabeledDir("Karthik")

	if _, err := os.Stat(trainningImagesDir); os.IsNotExist(err) {
		err := os.MkdirAll(trainningImagesDir, os.ModePerm)
		if err != nil {
			fmt.Println(err.Error())
		}
	}
	files, _ := ioutil.ReadDir(trainningImagesDir)
	fileCount := len(files)

	if fileCount >= 20 {
		return
	}

	pathComponents := []string{trainningImagesDir, "/image_", strconv.Itoa(fileCount + 1), ".jpg"}
	path := utills.JoinStrings(pathComponents)
	gocv.IMWrite(path, img)
}

func (v *Vision) TrainModel() {
	m := ModelTrainer{}
	m.trainModel()
}
