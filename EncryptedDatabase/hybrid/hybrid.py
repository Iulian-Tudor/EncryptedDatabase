import os
from encryption.encryption import Encryption


class HybridEncryption:
    @staticmethod
    def generate_symmetric_key():
        return os.urandom(32)

    @staticmethod
    def encrypt_symmetric_key(symmetric_key, public_key):
        return Encryption.encrypt_file(symmetric_key, public_key)

    @staticmethod
    def decrypt_symmetric_key(encrypted_symmetric_key, private_key):
        return Encryption.decrypt_file(encrypted_symmetric_key, private_key)

    @staticmethod
    def xor_encrypt_decrypt(input, key):
        return bytes([input_byte ^ key[i % len(key)] for i, input_byte in enumerate(input)])

    @staticmethod
    def encrypt_file_content(content, symmetric_key):
        return HybridEncryption.xor_encrypt_decrypt(content, symmetric_key)

    @staticmethod
    def decrypt_file_content(encrypted_content, symmetric_key):
        return HybridEncryption.xor_encrypt_decrypt(encrypted_content, symmetric_key)
