import os
from pymongo import MongoClient
from encryption import encrypt, decrypt


client = MongoClient('mongodb://localhost:27017/')
db = client['EncryptedDatabase']
collection = db['file_collection']

def add_file_to_database(file_path, public_key):
    with open(file_path, 'r') as file:
        content = file.read()

    encrypted_content = encrypt(public_key, content)

    data = {
        'file_path': file_path,
        'encrypted_content': encrypted_content
    }

    collection.insert_one(data)
    print("File added to the database.")

def get_file_from_database(file_path, private_key):
    file_data = collection.find_one({'file_path': file_path})

    if file_data:
        encrypted_content = file_data['encrypted_content']
        decrypted_content = decrypt(private_key, encrypted_content)

        print("\nDecrypted content:")
        print(decrypted_content)
    else:
        print("File not found in the database.")

def delete_file(file_path):
    result = collection.delete_one({'file_path': file_path})

    if result.deleted_count > 0:
        print("File deleted from the database.")
    else:
        print("File not found in the database.")

def view_database():
    files = collection.find()

    print("\nDatabase content:")
    for file in files:
        print(f"File: {file['file_path']}")