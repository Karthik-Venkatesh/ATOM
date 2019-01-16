#
#  frames.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:56 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

import cv2


def make_1080p(cap):
    cap.set(3, 1920)
    cap.set(4, 1080)


def make_720p(cap):
    cap.set(3, 1280)
    cap.set(4, 720)


def make_480p(cap):
    cap.set(3, 640)
    cap.set(4, 480)


def make_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


def rescale_frame(frame, percent=75):
    scale_percent = percent
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
