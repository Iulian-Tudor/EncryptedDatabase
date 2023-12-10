import os
from encryption.encryption import Encryption


class HybridEncryption:
    """
    Class for hybrid encryption.

    This class provides methods to generate a symmetric key, encrypt and decrypt the symmetric key,
    XOR encrypt and decrypt the file content, and encrypt and decrypt in an asymmetric way the key.
    """
    @staticmethod
    def generate_symmetric_key():
        """
        Generate a symmetric key.

        This method generates a symmetric key using os.urandom,
        and is called each time a new encryption takes place,
        so that the key is always different.
        """
        return os.urandom(32)

    @staticmethod
    def encrypt_symmetric_key(symmetric_key, public_key):
        """
        Encrypt the symmetric key.

        This method takes a symmetric key and a public key, and encrypts the symmetric key,
        using RSA asymmetric.
        """
        return Encryption.encrypt_file(symmetric_key, public_key)

    @staticmethod
    def decrypt_symmetric_key(encrypted_symmetric_key, private_key):
        """
        Decrypt the symmetric key.

        This method takes an encrypted symmetric key and a private key, and decrypts the symmetric key,
        using the same RSA algorithm.
        """
        return Encryption.decrypt_file(encrypted_symmetric_key, private_key)

    @staticmethod
    def xor_encrypt_decrypt(input, key):
        """
        XOR encrypt or decrypt input.

        This method takes an input and a key, and performs XOR encryption or decryption.
        """
        return bytes([input_byte ^ key[i % len(key)] for i, input_byte in enumerate(input)])

    @staticmethod
    def encrypt_file_content(content, symmetric_key):
        """
        Encrypt file content.

        This method takes content and a symmetric key, and encrypts the content,
        in a symmetric way.
        """
        return HybridEncryption.xor_encrypt_decrypt(content, symmetric_key)

    @staticmethod
    def decrypt_file_content(encrypted_content, symmetric_key):
        """
        Decrypt file content.

        This method takes encrypted content and a symmetric key, and decrypts the content,
        originally encrypted symmetrically.
        """
        return HybridEncryption.xor_encrypt_decrypt(encrypted_content, symmetric_key)
