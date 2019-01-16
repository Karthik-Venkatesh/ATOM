#
#  constant.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:54 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "..")

VISION_DIR = os.path.join(PROJECT_DIR, "vision")
MODEL_DIR = os.path.join(VISION_DIR, "model")
TRAINING_IMAGES_DIR = os.path.join(VISION_DIR, "training_images")

CASCADE_PATH = os.path.join(VISION_DIR, "cascades/data")
HAAR_CASCADE_PATH = os.path.join(CASCADE_PATH, "haarcascades")
HAARCASCADE_FRONTAL_FACE_ALT2 = os.path.join(HAAR_CASCADE_PATH, "haarcascade_frontalface_alt2.xml")

WAIT_KEY_MILLI_SECONDS = 20
DEFAULT_IMAGE_COUNT = 30
FRAME_SCALE_PERCENT = 50
