import os
import sys
import pickle
import imghdr
from pymongo import MongoClient

from encryption.encryption import Encryption
from hybrid.hybrid import HybridEncryption


class Database:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['EncryptedDatabase']
        self.collection = self.db['file_collection']

    def add_file_to_database(self, file_path, public_key, symmetric_key, encryption_method):
        proceed = True
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist.")
            proceed = False

        # Check if file is too large
        max_size = 10**8 #Max size of file in bytes
        if proceed and os.path.getsize(file_path) > max_size:
            print(f"File {file_path} is too large.")
            proceed = False

        # Check if file is empty
        if proceed and os.path.getsize(file_path) == 0:
            print(f"File {file_path} is empty.")
            proceed = False

        # Key validation
        e, n = public_key
        if proceed and not (1 < e < n):
            print("Invalid public key.")
            proceed = False

        if proceed:
            with open(file_path, 'rb') as file:
                content = file.read()
                if imghdr.what(file_path) is None:
                    print("Original content:")
                    print(content)

            encrypted_content = None
            encrypted_symmetric_key = None

            if encryption_method.lower() == 'rsa':
                encrypted_content = Encryption.encrypt_file(content, public_key)
            elif encryption_method.lower() == 'hybrid':
                encrypted_content = HybridEncryption.encrypt_file_content(content, symmetric_key)
                encrypted_symmetric_key = HybridEncryption.encrypt_symmetric_key(symmetric_key, public_key)
            else:
                print("Invalid encryption method.")
                proceed = False

            encrypted_content = pickle.dumps(encrypted_content)
            encrypted_directory = 'D:\\Anul3\\Python\\EncrypteDatabase\\EncryptedDatabase\\EncryptedTexts'

            encrypted_file_path = os.path.join(encrypted_directory, f"{os.path.basename(file_path)}.encrypted")
            with open(encrypted_file_path, 'wb') as encrypted_file:
                # Write the encrypted content directly to the file
                encrypted_file.write(encrypted_content)

            data = {
                'file_name': os.path.basename(file_path),
                'encrypted_file_path': encrypted_file_path,
                'encrypted_content': encrypted_content,
                'encryption_method' : encryption_method
            }

            if encryption_method.lower() == 'hybrid':
                data['encrypted_symmetric_key'] = encrypted_symmetric_key

            self.collection.insert_one(data)
            print("File added to the database.")

    def get_file_from_database(self, file_name, private_key, symmetric_key):
        file_data = self.collection.find_one({'file_name': file_name})

        if file_data:
            encrypted_content = file_data['encrypted_content']
            encryption_method = file_data['encryption_method']

            print("\nEncrypted content:")
            print(encrypted_content)

            encrypted_content = pickle.loads(encrypted_content)
            
            if encryption_method.lower() == 'rsa':
                decrypted_content = Encryption.decrypt_file(encrypted_content, private_key)
            elif encryption_method.lower() == 'hybrid':
                encrypted_symmetric_key = file_data['encrypted_symmetric_key']
                decrypted_symmetric_key = HybridEncryption.decrypt_symmetric_key(encrypted_symmetric_key, private_key)
                decrypted_content = HybridEncryption.decrypt_file_content(encrypted_content, decrypted_symmetric_key)
            else:
                print("Invalid encryption method.")
                return

            try:
                print("\nDecrypted content:")
                print(decrypted_content.decode('utf-8'))
            except UnicodeDecodeError:
                print("\nDecrypted content is not valid UTF-8 text and cannot be printed to terminal.")

            decrypted_directory = 'D:\\Anul3\\Python\\EncrypteDatabase\\EncryptedDatabase\\DecryptedTexts'
            decrypted_file_path = os.path.join(decrypted_directory, f"decrypted_{file_name}")

            with open(decrypted_file_path, 'wb') as output_file:
                output_file.write(decrypted_content)

        else:
            print("File not found in the database.")

    def delete_file(self, file_names):
        for file_name in file_names:
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

    def delete_all_files(self):
        self.collection.delete_many({})
        print("All files deleted from the database.")

    def view_database(self):
        files = self.collection.find()

        print("\nDatabase content:")
        for file in files:
            file_name = file.get('file_name', 'N/A')
            encrypted_file_path = file.get('encrypted_file_path', 'N/A')
            print(f"File name: {file_name}, encrypted file path: {encrypted_file_path}")
