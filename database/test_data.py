from pymongo import MongoClient

atom_db_client = MongoClient('mongodb://localhost:27017/')
atom_db = atom_db_client["atom"]
faces_col = atom_db["faces"]
faces_info_col = atom_db["label"]

for document in faces_col.find():
    print (document)

for document in faces_info_col.find():
    print (document)