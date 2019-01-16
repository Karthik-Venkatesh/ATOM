#
#  computer_vision.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:56 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

import cv2
import os
from vision import frames
from vision.model_trainer import ModelTrainer
import pickle
from constants import constant


class ComputerVision:

    cap = cv2.VideoCapture(0)
    labels = {}
    recognizer = None
    model_folder_path = None
    image_count: int = 0
    cascade_classifier = cv2.CascadeClassifier(constant.HAARCASCADE_FRONTAL_FACE_ALT2)

    def __init__(self):
        print("Computer Vision Instantiated...")
        print(constant.HAARCASCADE_FRONTAL_FACE_ALT2)
        self.load_latest_model()

    def start_recording(self):
        print("Computer Vision Started...")
        while True:
            ret, frame = self.cap.read()
            frame = frames.rescale_frame(frame, percent=constant.FRAME_SCALE_PERCENT)

            if self.model_folder_path is not None:
                if self.save_faces(frame, self.model_folder_path) is False:
                    self.model_folder_path = None
                    self.train_model()

            self.predict_faces(frame)
            self.show_rect(frame)

            cv2.imshow('frame', frame)

            wait_key = cv2.waitKey(constant.WAIT_KEY_MILLI_SECONDS)

            if wait_key == ord('q'):
                self.stop_recording()
                break

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")

    def add_face(self, label: str):
        self.model_folder_path = os.path.join(constant.TRAINING_IMAGES_DIR, label)
        if os.path.exists(self.model_folder_path):
            self.image_count = len(os.listdir(self.model_folder_path))
        else:
            self.image_count = 0

    def save_faces(self, frame, model_folder_path):

        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        files = os.listdir(model_folder_path)
        file_count = len(files)

        if file_count >= (self.image_count + constant.DEFAULT_IMAGE_COUNT):
            return False

        faces = self.cascade_classifier.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        img_item = model_folder_path + "/" + str(file_count + 1) + ".jpg"

        if len(faces) > 0:
            cv2.imwrite(img_item, frame)

        return True

    def train_model(self):
        self.model_folder_path = None

        trainer = ModelTrainer()
        if trainer.train_model():
            trainer.save_model()
            self.load_latest_model()
        else:
            print("Error: Model training failed...")

    def load_latest_model(self):
        latest_model_dir = constant.MODEL_DIR
        if not latest_model_dir:
            return
        trainer_file = latest_model_dir + "/" + "trainer.yml"
        pickle_file = latest_model_dir + "/" + "labels.pickle"
        if os.path.exists(trainer_file) & os.path.exists(pickle_file):
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(trainer_file)

            with open(pickle_file, "rb") as f:
                og_labels = pickle.load(f)
                self.labels = {v: k for k, v in og_labels.items()}
        else:
            self.recognizer = None
            self.labels = {}

    def predict_faces(self, frame):

        if self.recognizer is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade_classifier.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y: y+h, x: x+w]

            id_, conf = self.recognizer.predict(roi_gray)
            if conf < 45:
                print("label_id: ", id_)
                print("label: ", self.labels[id_])

    def show_rect(self, frame, faces=None):

        if faces is None:
            faces = self.cascade_classifier.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            color = (255, 0, 0)
            stroke = 2
            end_coord_x = x + w
            end_coord_y = y + h
            cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), color, stroke)
