import os
from rsa.rsa import Encryption


class HybridEncryption:
    """
    Class for hybrid encryption.

    This class provides methods to generate a symmetric key, encrypt and decrypt the symmetric key,
    XOR encrypt and decrypt the file content, and encrypt and decrypt in an asymmetric way the key.
    """
    @staticmethod
    def generate_symmetric_key() -> bytes:
        """
        Generate a symmetric key.

        This method generates a symmetric key using os.urandom,
        and is called each time a new encryption takes place,
        so that the key is always different.

        Returns:
        bytes: The symmetric key generated.
        """
        return os.urandom(32)

    @staticmethod
    def encrypt_symmetric_key(symmetric_key:bytes, public_key:tuple) -> list[int]:
        """
        Encrypt the symmetric key.

        This method takes a symmetric key and a public key, and encrypts the symmetric key,
        using RSA asymmetric.

        Parameters:
        symmetric_key (bytes): The symmetric key to be encrypted.
        public_key (tuple): The public key to be used for encryption.

        Returns:
        list[int]: The encrypted symmetric key.
        """
        return Encryption.encrypt_file(symmetric_key, public_key)

    @staticmethod
    def decrypt_symmetric_key(encrypted_symmetric_key:bytes, private_key:tuple) -> bytes:
        """
        Decrypt the symmetric key.

        This method takes an encrypted symmetric key and a private key, and decrypts the symmetric key,
        using the same RSA algorithm.

        Parameters:
        encrypted_symmetric_key (bytes): The encrypted symmetric key to be decrypted.
        private_key (tuple): The private key to be used for decryption.

        Returns:
        bytes: The decrypted symmetric key.
        """
        return Encryption.decrypt_file(encrypted_symmetric_key, private_key)

    @staticmethod
    def xor_encrypt_decrypt(input:bytes, key:bytes) -> bytes:
        """
        XOR encrypt or decrypt input.

        This method takes an input and a key, and performs XOR encryption or decryption.

        Parameters:
        input (bytes): The input to be encrypted or decrypted.
        key (bytes): The key to be used for encryption or decryption.

        Returns:
        bytes: The encrypted or decrypted input.
        """
        return bytes([input_byte ^ key[i % len(key)] for i, input_byte in enumerate(input)])

    @staticmethod
    def encrypt_file_content(content:bytes, symmetric_key:bytes) -> bytes:
        """
        Encrypt file content.

        This method takes content and a symmetric key, and encrypts the content,
        in a symmetric way.

        Parameters:
        content (bytes): The content to be encrypted.
        symmetric_key (bytes): The symmetric key to be used for encryption.

        Returns:
        bytes: The encrypted content.
        """
        return HybridEncryption.xor_encrypt_decrypt(content, symmetric_key)

    @staticmethod
    def decrypt_file_content(encrypted_content:bytes, symmetric_key:bytes) -> bytes:
        """
        Decrypt file content.

        This method takes encrypted content and a symmetric key, and decrypts the content,
        originally encrypted symmetrically.

        Parameters:
        encrypted_content (bytes): The encrypted content to be decrypted.
        symmetric_key (bytes): The symmetric key to be used for decryption.

        Returns:
        bytes: The decrypted content.
        """
        return HybridEncryption.xor_encrypt_decrypt(encrypted_content, symmetric_key)
