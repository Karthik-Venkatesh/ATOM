/*
 * vision.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Mon Feb 04 2019 9:27:24 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

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
