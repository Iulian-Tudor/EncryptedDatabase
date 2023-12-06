import os
from pymongo import MongoClient
from encryption.encryption import Encryption


class Database:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['EncryptedDatabase']
        self.collection = self.db['file_collection']
        
    @staticmethod
    def add_file_to_database(self, file_path, public_key):
        with open(file_path, 'r') as file:
            content = file.read()
            print("Original content:")
            print(content)

        encrypted_content = Encryption.encrypt_file(content, public_key)
        encrypted_directory = 'D:\\Anul3\\Python\\EncryptedTexts'

        encrypted_file_path = os.path.join(encrypted_directory, f"{os.path.basename(file_path)}.encrypted")
        with open(encrypted_file_path, 'wb') as encrypted_file:
            # Write the encrypted content directly to the file
            encrypted_file.write(encrypted_content.encode())

        data = {
            'file_name': os.path.basename(file_path),
            'encrypted_file_path': encrypted_file_path,
            'encrypted_content': encrypted_content
        }

        self.collection.insert_one(data)
        print("File added to the database.")

    @staticmethod
    def get_file_from_database(self, file_name, private_key):
        file_data = self.collection.find_one({'file_name': file_name})

        if file_data:
            encrypted_content = file_data['encrypted_content']

            print("\nEncrypted content:")
            print(encrypted_content)

            decrypted_content = Encryption.decrypt_file(encrypted_content, private_key)

            print('\nDecrypted content: ASCII')
            for char in decrypted_content:
                print(ord(char), end=' ')

            print("\nDecrypted content:")
            print(decrypted_content)

            with open('decrypted_file.txt', 'w') as output_file:
                output_file.write(decrypted_content)

        else:
            print("File not found in the database.")

    @staticmethod
    def delete_file(self, file_name):
        file_data = self.collection.find_one({'file_name': file_name})

        if file_data:
            # Delete from the local encrypted directory
            encrypted_file_path = file_data['encrypted_file_path']
            os.remove(encrypted_file_path)

            # Delete from the database
            result = self.collection.delete_one({'file_name': file_name})

            if result.deleted_count > 0:
                print("File deleted from the database and local directory.")
            else:
                print("File found in the local directory but not deleted from the database.")
        else:
            print("File not found in the database.")

    @staticmethod
    def view_database(self):
        files = self.collection.find()

        print("\nDatabase content:")
        for file in files:
            file_name = file.get('file_name', 'N/A')
            print(f"File: {file_name}")
