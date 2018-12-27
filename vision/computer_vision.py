import cv2
import numpy as np
import os
from vision import frames

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAARCASCADE_FRONTAL_FACE_ALT2 = cv2.CascadeClassifier(BASE_DIR + "/cascades/data/haarcascade_frontalface_alt2.xml")

class ComputerVision:

    cap = cv2.VideoCapture(0)
    save_face = True

    def __init__(self):
        print("Computer Vision Instantiated...")

    def start_recording(self):
        print("Computer Vision Started...")
        while True:
            ret, frame = self.cap.read()
            frame = frames.rescale_frame(frame, percent=30)

            if self.save_face:
                self.save_faces(frame, "myImage")

            cv2.imshow('frame', frame)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")

    def save_faces(self, frame, folder_name):

        image_dir = os.path.join(BASE_DIR, "trainning_images" + "/" + folder_name)

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        files = os.listdir(image_dir)
        file_count = len(files)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        img_item = image_dir + "/" + str(file_count + 1) + ".jpg"

        for (x, y, w, h) in faces:
            roi_face = frame[y: y+h, x: x+w]
            cv2.imwrite(img_item, roi_face)
