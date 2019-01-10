import os

from PIL import Image
import numpy as np
from numpy.core.multiarray import ndarray
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(BASE_DIR, "cascades/data")


class ModelTrainer:

    face_cascade = cv2.CascadeClassifier(CASCADE_PATH + "/haarcascades/haarcascade_frontalface_alt2.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    x_train = []
    y_labels = []

    def train_model(self):
        training_images_dir = os.path.join(BASE_DIR, "training_images")
        for root, dirs, files in os.walk(training_images_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()
                    if label not in self.label_ids:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    id_ = self.label_ids[label]

                    pil_image = Image.open(path).convert('L')  # Grayscale
                    image_array: ndarray = np.array(pil_image, "uint8")
                    faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                    '''
                    # Another way of getting faces.

                    img = cv2.imread(path)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
                    '''
                    for (x, y, w, h) in faces:
                        roi = image_array[y: y + h, x: x + w]
                        self.x_train.append(roi)
                        self.y_labels.append(id_)

        if not self.x_train:
            return False
        else:
            return True

    def save_model(self):
        model_dir = os.path.join(BASE_DIR, "model")

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        with open(model_dir + "/" + "labels.pickle", "wb") as f:
            pickle.dump(self.label_ids, f)

        self.recognizer.train(self.x_train, np.array(self.y_labels))
        self.recognizer.save(model_dir + "/" + "trainer.yml")

        # https://github.com/Karthik-Venkatesh/atom/issues/13
        # self.delete_trained_images()

    @staticmethod
    def delete_trained_images():
        # images_dir = os.path.join(BASE_DIR, "training_images")
        # shutil.rmtree(images_dir)
        print("Deleting trained images be implemented in feature")
        print("For detail check latest comment on github issue: https://github.com/Karthik-Venkatesh/atom/issues/13")
