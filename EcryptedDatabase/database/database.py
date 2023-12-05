import os
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['EncryptedDatabase']

def add_file_to_database(ecrypted_file_path, symmetric_key, public_key, n):
    with open(ecrypted_file_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = encrypt_message(file_data, symmetric_key, public_key, n)

    db.files.insert_one({'file_path': encrypted_file_path, 'encryption_method': 'encryption_method'})




def read_file_from_database(encrypted_file_path, symmetric_key, private_key, n):
    file_info = db.files.find_one({'file_path': encrypted_file_path})

    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = decrypt_message(encrypted_data, symmetric_key, private_key, n)

    return decrypted_data


def delete_from_database(encrypted_file_path):
    db.files.delete_one({'file_path': encrypted_file_path})

    os.remove(encrypted_file_path)