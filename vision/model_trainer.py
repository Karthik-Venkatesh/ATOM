import os
from PIL import Image
import numpy as np
from numpy.core.multiarray import ndarray
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class ModelTrainer:

    face_cascade = cv2.CascadeClassifier(BASE_DIR + '/cascades/data/haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    x_train = []
    y_labels = []

    def train_model(self):
        trainning_images_dir = os.path.join(BASE_DIR, "training_images")
        for root, dirs, files in os.walk(trainning_images_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()
                    if not label in self.label_ids:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1
                    id_ = self.label_ids[label]

                    pil_image = Image.open(path).convert("L")  # Grayscale
                    image_array: ndarray = np.array(pil_image, "uint8")

                    faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

                    for (x, y, w, h) in faces:
                        roi = image_array[y: y + h, x: x + w]
                        self.x_train.append(roi)
                        self.y_labels.append(id_)

    def save_model(self):
        models_dir = os.path.join(BASE_DIR, "models")

        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        files = os.listdir(models_dir)
        version = len(files) +1
        model_dir = os.path.join(models_dir, "version_" + str(version))
        os.makedirs(model_dir)

        with open(model_dir + "/" + "labels.pickle", "wb") as f:
            pickle.dump(self.label_ids, f)

        self.recognizer.train(self.x_train, np.array(self.y_labels))
        self.recognizer.save(model_dir + "/" + "trainer.yml")