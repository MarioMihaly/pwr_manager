'''
    Notes for implementation
    src: https://support.itglue.com/hc/en-us/articles/360004938438-About-password-security-and-encryption
    -> AES 256 - unique AES key is generated for each encrypted password
    -> 2048 bit RSA key pair to encrypt the AES 256 keys

'''

import config

from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256


class AES_encryption:
    def __init__(self, password):
        self.key = str_to_SHA(password)

    def pad(self, message):
        return message.encode() + b"\0" * (AES.block_size - len(message) % AES.block_size)

    def encrypt(self, message):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0").decode()

def str_to_SHA(s):
    return SHA256.new(data=s.encode()).digest()