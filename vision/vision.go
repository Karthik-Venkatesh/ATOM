package vision

import (
	"fmt"
	"image"
	"image/color"
	"path"
	"runtime"

	"gocv.io/x/gocv"
)

type Vision struct {
	videoCapture *gocv.VideoCapture
	window       *gocv.Window
}

func NewVision() *Vision {
	v := Vision{}
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
	classifier, e := v.frontalFaceClassifier()
	if e != nil {
		fmt.Printf(e.Error())
	}

	for {
		if ok := v.videoCapture.Read(&img); !ok {
			return
		}
		if img.Empty() {
			continue
		}

		// detect faces
		rects := classifier.DetectMultiScaleWithParams(img, 1.1, 5, 0, image.Point{X: 100, Y: 100}, image.Point{X: 500, Y: 500})
		fmt.Printf("found %d faces\n", len(rects))

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

func (v *Vision) frontalFaceClassifier() (c gocv.CascadeClassifier, e error) {
	// load classifier to recognize faces
	_, filename, _, _ := runtime.Caller(1)
	c = gocv.NewCascadeClassifier()
	cascadePath := path.Join(path.Dir(filename), "cascades/data/haarcascades/haarcascade_frontalface_alt2.xml")
	success := c.Load(cascadePath)
	if success {
		return c, nil
	}
	e = fmt.Errorf("Error: haarcascade_frontalface_alt2 laoding xml")
	return c, e
}
