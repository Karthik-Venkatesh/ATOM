from pymongo import MongoClient
from numpy.core.multiarray import ndarray

atom_db_client = MongoClient('mongodb://localhost:27017/')
atom_db = atom_db_client["atom"]
faces_col = atom_db["faces"]
faces_info_col = atom_db["labels"]


def save_face_trainning_data(x_train: [], y_train: [], labels: {}):
    face_data = []
    for idx, val in enumerate(x_train):
        y_label = y_train[idx]
        label = list(labels.keys())[list(labels.values()).index(y_label)]
        label_id = label.replace(' ', '').lower()
        face = {"faceData": x_train[idx].tolist(), "faceId": label_id, "label": label}
        face_data.append(face)
    faces_col.insert_many(face_data)

    faces_info = []
    for key, value in labels.items():
        label = key
        label_id = label.replace(' ', '').lower()
        faces_info.append({"faceId": label_id, "label": label})
    faces_info_col.insert_many(faces_info)

