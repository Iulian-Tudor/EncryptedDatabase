import os
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['EncryptedDatabase']
collection = db['file_collection']

def add_file_to_database(filename, public_key):
    with open(filename, 'r') as file:
        content = file.read()

    encrypted_content = encrypt(content, public_key)

    with open(filename + '.enc', 'w') as file:
        file.write(''.join(map(lambda x: str(x), encrypted_content)))

    collection.insert_one({
        'filename': filename,
        'location': filename + '.enc'
        'public_key': public_key
    })


def get_file_from_database(filename, private_key):
    file_data = collection.find_one({'filename': filename})

    with open(file_data['location'], 'r') as file:
        encrypted_content = list(map(lambda x: int(x), file.readlines()))

        content = decrypt(private_key, encrypted_content)
        print(content)


def delete_file(filename):
    file_data = collection.find_one({'filename': filename})
    os.remove(file_data['location'])
    collection.delete_one({'filename': filename})