import random

def gcd (a,b):
    while b != 0:
        a, b = b, a % b
    return a

def invers_multiplicativ(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi
    

def key_generator(p, q):
    n = p * q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = invers_multiplicativ(e, phi)

    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    e, n = pk
    cipher = [(ord(char) ** e) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    d, n = pk
    plaintext = [chr((char ** d) % n) for char in ciphertext]
    return ''.join(plaintext)
