/*
 * sp.go
 * ATOM
 *
 * Created by Karthik V
 * Created on Fri Feb 08 2019 9:51:13 PM
 *
 * Copyright © 2019 Karthik Venkatesh. All rights reserved.
 */

package utills

import (
	"bytes"
)

func JoinStrings(arr []string) string {
	var buffer bytes.Buffer
	for index := 0; index < len(arr); index++ {
		buffer.WriteString(arr[index])
	}
	ns := buffer.String()
	return ns
}

func RemoveDuplicateStrings(s []string) []string {
	m := make(map[string]bool)
	for _, item := range s {
		if _, ok := m[item]; ok {
			// duplicate item
		} else {
			m[item] = true
		}
	}

	var result []string
	for item := range m {
		result = append(result, item)
	}
	return result
}
