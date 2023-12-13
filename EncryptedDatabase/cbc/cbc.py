import os
from hybrid.hybrid import HybridEncryption

class CBC:
    BLOCK_SIZE = 32

    @staticmethod
    def generate_symmetric_key() -> bytes:
        """
        Generates a symmetric key. In a production environment, this should be generated
        carefully with a cryptographically secure random number generator.

        Returns:
        bytes: The symmetric key.
        """
        return os.urandom(CBC.BLOCK_SIZE)

    @staticmethod
    def generate_iv() -> bytes:
        """
        Generates a random initialization vector. In a production environment, this should be generated
        carefully with a cryptographically secure random number generator, because it's the most important
        and vulnerable part of the encryption scheme.

        Returns:
        bytes: The initialization vector.
        """
        return os.urandom(CBC.BLOCK_SIZE)
    
    @staticmethod
    def xor_bytes(a: bytes, b: bytes) -> bytes:
        """
        XORs two byte strings together. If the byte strings are of different lengths, the shorter one is padded.

        Args:
        a (bytes): The first byte array.
        b (bytes): The second byte array.

        Returns:
        bytes: The XORed byte array.
        """
        if len(a) < len(b):
            a += b'\0' * (len(b) - len(a))
        elif len(b) < len(a):
            b += b'\0' * (len(a) - len(b))

        return bytes([x ^ y for x, y in zip(a, b)])
    

    @staticmethod
    def pad(plaintext: bytes) -> bytes:
        """
        Pads a plaintext to be a multiple of the block size.

        Args:
        plaintext (bytes): The plaintext to pad.

        Returns:
        bytes: The padded plaintext.
        """
        padding_length = CBC.BLOCK_SIZE - len(plaintext) % CBC.BLOCK_SIZE
        padding = bytes([padding_length] * padding_length)
        return plaintext + padding
    
    @staticmethod
    def unpad(plaintext: bytes) -> bytes:
        """
        Unpads a plaintext.

        Args:
        plaintext (bytes): The plaintext to unpad.

        Returns:
        bytes: The unpadded plaintext.
        """
        padding_length = plaintext[-1]
        return plaintext[:-padding_length]
    
    @staticmethod
    def encrypt_block(plaintext: bytes, symmetric_key: bytes, iv: bytes) -> bytes:
        """
        Encrypts a block of plaintext.

        Paremters:
        plaintext (bytes): The plaintext to encrypt.
        symmetric_key (bytes): The symmetric key to use for encryption.
        iv (bytes): The initialization vector to use for encryption.

        Returns:
        bytes: The encrypted block.
        """
        plaintext = CBC.pad(plaintext)
        xor_result = CBC.xor_bytes(plaintext, iv)
        return CBC.xor_bytes(xor_result, symmetric_key)

    @staticmethod
    def decrypt_block(ciphertext: bytes, symmetric_key: bytes, iv: bytes) -> bytes:
        """
        Decrypts a block of ciphertext.

        Parameters:
        ciphertext (bytes): The ciphertext to decrypt.
        symmetric_key (bytes): The symmetric key to use for decryption.
        iv (bytes): The initialization vector to use for decryption.

        Returns:
        bytes: The decrypted block.
        """
        decrypted = CBC.xor_bytes(ciphertext, symmetric_key)
        return CBC.unpad(CBC.xor_bytes(decrypted, iv))
    
    @staticmethod
    def encrypt_message(plaintext: bytes, symmetric_key: bytes, iv: bytes) -> bytes:
        """
        Encrypts the message, block-by-block.

        Parameters:
        plaintext (bytes): The plaintext to encrypt.
        symmetric_key (bytes): The symmetric key to use for encryption.
        iv (bytes): The initialization vector to use for encryption, that is updated for each block.

        Returns:
        bytes: The encrypted message.
        """
        ciphertext = b""
        for i in range(0, len(plaintext), CBC.BLOCK_SIZE):
            block = plaintext[i:i+CBC.BLOCK_SIZE]
            encrypted_block = CBC.encrypt_block(block, symmetric_key, iv)
            ciphertext += encrypted_block
            iv = encrypted_block  # Update the IV for the next block
        return ciphertext

    @staticmethod
    def decrypt_message(ciphertext: bytes, symmetric_key: bytes, iv: bytes) -> bytes:
        """
        Decrypts the message, block-by-block.

        Parameters:
        ciphertext (bytes): The ciphertext to decrypt.
        symmetric_key (bytes): The symmetric key to use for decryption.
        iv (bytes): The initialization vector to use for decryption, that is updated for each block.

        Returns:
        bytes: The decrypted message.
        """
        plaintext = b""
        for i in range(0, len(ciphertext), CBC.BLOCK_SIZE):
            block = ciphertext[i:i+CBC.BLOCK_SIZE]
            decrypted_block = CBC.decrypt_block(block, symmetric_key, iv)
            plaintext += decrypted_block
            iv = block  # Update the IV for the next block
        return plaintext