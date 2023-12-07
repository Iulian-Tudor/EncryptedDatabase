from math import gcd


# Function to find the greatest common divisor
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# Function to produce the private-key exponent
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


class Encryption:
    @staticmethod
    def generate_key_pair(p, q):
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
    def encrypt_file(content, public_key):
    # Encrypt the file content using the public key
        e, n = public_key
        return [(byte ** e) % n for byte in content]

    @staticmethod
    def decrypt_file(encrypted_content, private_key):
    # Decrypt the file content using the private key
        d, n = private_key
        return bytes((byte ** d) % n for byte in encrypted_content)