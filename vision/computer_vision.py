import cv2
import os
from vision import frames
from vision.model_trainer import ModelTrainer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAARCASCADE_FRONTAL_FACE_ALT2 = cv2.CascadeClassifier(BASE_DIR + "/cascades/data/haarcascade_frontalface_alt2.xml")
WAIT_KEY_MILLI_SECONDS = 20


class ComputerVision:

    cap = cv2.VideoCapture(0)
    save_face = False

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

            wait_key = cv2.waitKey(WAIT_KEY_MILLI_SECONDS)

            if wait_key == ord('q'):
                break
            elif wait_key == ord('s'):
                self.save_face = True
            elif wait_key == ord('d'):
                self.save_face = False
                trainer = ModelTrainer()
                trainer.train_model()
                trainer.save_model()

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")

    def save_faces(self, frame, folder_name):

        image_dir = os.path.join(BASE_DIR, "training_images" + "/" + folder_name)

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        files = os.listdir(image_dir)
        file_count = len(files)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        img_item = image_dir + "/" + str(file_count + 1) + ".jpg"

        for (x, y, w, h) in faces:
            roi_face = gray[y: y+h, x: x+w]
            cv2.imwrite(img_item, roi_face)
