package vision

import (
	"gocv.io/x/gocv"
)

type Vision struct {
}

func (v *Vision) StartVision() {
	webcam, _ := gocv.VideoCaptureDevice(0)
	window := gocv.NewWindow("Hello")
	img := gocv.NewMat()

	for {
		webcam.Read(&img)
		window.IMShow(img)
		window.WaitKey(1)
	}
}

func main() {

}
