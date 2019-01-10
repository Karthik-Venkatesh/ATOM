import cv2
import os
from vision import frames
from vision.model_trainer import ModelTrainer
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(BASE_DIR, "/cascades/data")
HAARCASCADE_FRONTAL_FACE_ALT2 = cv2.CascadeClassifier(CASCADE_PATH + "/haarcascades/haarcascade_frontalface_alt2.xml")
WAIT_KEY_MILLI_SECONDS = 20
DEFAULT_IMAGE_COUNT = 30


class ComputerVision:

    cap = cv2.VideoCapture(0)
    labels = {}
    recognizer = None
    model_folder_path = None
    faces_count: int = 0

    def __init__(self):
        print("Computer Vision Instantiated...")
        self.load_latest_model()

    def start_recording(self):
        print("Computer Vision Started...")
        while True:
            ret, frame = self.cap.read()
            frame = frames.rescale_frame(frame, percent=30)

            if self.model_folder_path is not None:
                if self.save_faces(frame, self.model_folder_path) is False:
                    self.model_folder_path = None
                    self.train_model()

            self.predict_faces(frame)

            cv2.imshow('frame', frame)

            wait_key = cv2.waitKey(WAIT_KEY_MILLI_SECONDS)

            if wait_key == ord('q'):
                self.stop_recording()
                break

    def stop_recording(self):
        cv2.destroyWindow(self.cap)
        print("Computer Vision Stopped...")

    def add_face(self, label: str):
        self.model_folder_path = os.path.join(BASE_DIR, "training_images" + "/" + label)

    def save_faces(self, frame, model_folder_path):

        image_dir = model_folder_path

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        files = os.listdir(image_dir)
        file_count = len(files)

        if self.faces_count >= DEFAULT_IMAGE_COUNT:
            self.faces_count = 0
            return False
        else:
            self.faces_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        img_item = image_dir + "/" + str(file_count + 1) + ".jpg"

        for (x, y, w, h) in faces:
            roi_face = gray[y: y+h, x: x+w]
            cv2.imwrite(img_item, roi_face)

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
                self.labels = {v: k for k, v in og_labels.items()}
        else:
            self.recognizer = None
            self.labels = {}

    def predict_faces(self, frame):

        if self.recognizer is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y: y+h, x: x+w]

            id_, conf = self.recognizer.predict(roi_gray)
            if conf > 45:
                print("label_id: ", id_)
                print("label: ", self.labels[id_])

    @staticmethod
    def show_rect(frame, faces=None):
        
        if faces is None:
            faces = HAARCASCADE_FRONTAL_FACE_ALT2.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            color = (255, 0, 0)
            stroke = 2
            end_coord_x = x + w
            end_coord_y = y + h
            cv2.rectangle(frame, (x, y), (end_coord_x, end_coord_y), color, stroke)
