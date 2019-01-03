import cv2
import os
from vision import frames
from vision.model_trainer import ModelTrainer
import pickle
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAARCASCADE_FRONTAL_FACE_ALT2 = cv2.CascadeClassifier(BASE_DIR + "/cascades/data/haarcascade_frontalface_alt2.xml")
WAIT_KEY_MILLI_SECONDS = 20
DEFAULT_IMAGE_COUNT = 30

class ComputerVision:

    cap = cv2.VideoCapture(0)
    save_face = False
    labels = {}
    recognizer = None

    def __init__(self):
        print("Computer Vision Instantiated...")
        self.load_latest_model()

    def start_recording(self):
        print("Computer Vision Started...")
        while True:
            ret, frame = self.cap.read()
            frame = frames.rescale_frame(frame, percent=30)

            model_folder_name = "myImage"
            model_folder_path = os.path.join(BASE_DIR, "training_images" + "/" + model_folder_name)

            if self.save_face:
                if self.save_faces(frame, model_folder_path) == False:
                    self.save_face = False
                    self.train_model()

            self.predict_faces(frame)

            cv2.imshow('frame', frame)

            wait_key = cv2.waitKey(WAIT_KEY_MILLI_SECONDS)

            if wait_key == ord('q'):
                break
            elif wait_key == ord('s'):
                if os.path.exists(model_folder_path):
                    shutil.rmtree(model_folder_path)
                self.save_face = True

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")

    def save_faces(self, frame, model_folder_path):

        image_dir = model_folder_path

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        files = os.listdir(image_dir)
        file_count = len(files)

        if file_count >= DEFAULT_IMAGE_COUNT:
            return False

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        img_item = image_dir + "/" + str(file_count + 1) + ".jpg"

        for (x, y, w, h) in faces:
            roi_face = gray[y: y+h, x: x+w]
            cv2.imwrite(img_item, roi_face)

        return True

    def train_model(self):
        trainer = ModelTrainer()
        if trainer.train_model():
            trainer.save_model()
            self.load_latest_model()
        else:
            print("Error: Model trainning failed...")

    def load_latest_model(self):
        latest_model_dir = os.path.join(BASE_DIR, "model")
        if not latest_model_dir:
            return
        trainer_file = latest_model_dir + "/" + "trainer.yml"
        pickle_file = latest_model_dir + "/" + "labels.pickle"
        if os.path.exists(trainer_file) & os.path.exists(pickle_file):
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(trainer_file)

            with open(pickle_file, "rb") as f:
                og_labels = pickle.load(f)
                self.labels = {v:k for k,v in og_labels.items()}
        else:
            self.recognizer = None
            self.labels = {}

    def predict_faces(self, frame):

        if self.recognizer == None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y: y+h, x: x+w]
            roi_color = frame[y: y+h, x: x+w]

            id_, conf = self.recognizer.predict(roi_gray)
            if conf > 45:
                print("label_id: ", id_)
                print("label: ", self.labels[id_])
