from math import gcd


# Function to find the greatest common divisor
def extended_gcd(aa:int, bb:int) -> tuple:
    """
    Function to find the greatest common divisor (gcd).

    This function uses the Extended Euclidean Algorithm to find the gcd of two numbers aa and bb.
    It also finds the coefficients x and y in the equation: gcd(aa, bb) = aa*x + bb*y.
    The Extended Euclidean Algorithm is particularly useful when aa and bb are large numbers.

    Parameters:
    aa (int): The first number.
    bb (int): The second number.

    Returns:
    tuple: A tuple containing the gcd and the coefficients x and y.
    """
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# Function to produce the private-key exponent
def modinv(a, m) -> int:
    """
    Function to produce the private-key exponent.

    This function uses the Extended Euclidean Algorithm to find the multiplicative inverse of a modulo m.
    The multiplicative inverse of a modulo m is a number x such that (a*x) % m = 1.
    This is used in the RSA algorithm to generate the private key.

    Parameters:
    a (int): The number for which to find the multiplicative inverse.
    m (int): The modulo.

    Returns:
    int: The multiplicative inverse of a modulo m.
    """
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


class Encryption:
    """
    Class for encryption.

    This class provides methods to generate a key pair, encrypt a file, and decrypt a file,
    with asymmetric RSA.
    """
    @staticmethod
    def generate_key_pair(p:int, q:int) -> tuple:
        """
        Generate a public and private key pair.

        This method takes two prime numbers, p and q, and generates a public and private key pair.
        The RSA modulus is calculated as the product of p and q.
        The totient is calculated as the product of (p-1) and (q-1).

        The totient is the number of co-prime numbers with n, smaller than n and greater than 1.
        The public exponent is calculated as the first number e, greater than 2, such that gcd(e, totient) = 1.
        The private exponent is calculated as the multiplicative inverse of the public exponent modulo totient.

        Parameters:
        p (int): The first prime number.
        q (int): The second prime number.

        Returns:
        tuple: A tuple containing the public and private key pair.
        """
        # Generate a public and private key pair
        RSA_modulus = p * q
        totient = (p - 1) * (q - 1)
        public_exponent = 0
        for e in range(3, totient - 1):
            if gcd(e, totient) == 1:
                public_exponent = e
                break
        private_exponent = modinv(public_exponent, totient)
        return (public_exponent, RSA_modulus), (private_exponent, RSA_modulus)

    @staticmethod
    def encrypt_file(content:bytes, public_key:tuple) -> list[int]:
        """
        Encrypt the file content using the public key.

        This method takes the content of a file and a public key, and encrypts the content,
        asymmetrically, with RSA.

        Parameters:
        content (bytes): The content of the file to be encrypted.
        public_key (tuple): The public key to be used for encryption.

        Returns:
        list[int]: The encrypted content of the file.
        """
        # Encrypt the file content using the public key
        e, n = public_key
        return [(byte ** e) % n for byte in content]

    @staticmethod
    def decrypt_file(encrypted_content:bytes, private_key:tuple) -> bytes:
        """
        Decrypt the file content using the private key.

        This method takes the encrypted content of a file and a private key, and decrypts the content,
        doing the reverse of the encryption process.

        Parameters:
        encrypted_content (bytes): The encrypted content of the file to be decrypted.
        private_key (tuple): The private key to be used for decryption.

        Returns:
        bytes: The decrypted content of the file.
        """
        # Decrypt the file content using the private key
        d, n = private_key
        return bytes((byte ** d) % n for byte in encrypted_content)
