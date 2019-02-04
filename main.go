package main

import (
	"fmt"

	"github.com/ATOM/vision"
)

func main() {
	fmt.Println("ATOM...")
	v := vision.NewVision()
	v.StartVision()
}
