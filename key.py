import base64
import hashlib
import os

import cryptography.hazmat.primitives.asymmetric.padding as pad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AllMethods:

    @staticmethod
    def gen_aes_key():
        return os.urandom(32)

    @staticmethod
    def aes_encrypt(key, file_path):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        plaintext = open(file_path, 'rb').read()
        padded_data = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv, ciphertext

    @staticmethod
    def generate_method(key_file):
        with open(key_file, 'rb') as f:
            method = f.readline().strip()
        if method == b'AES':
            return 0
        elif method == b'ECC':
            return 1
        elif method == b'PBKDF2':
            return 2
        elif method == b'SHA':
            return 3
        else:
            return ValueError("Method is not valid!")

    @staticmethod
    def aes_decrypt(key_file, encrypt_file):
        with open(key_file, 'rb') as f:
            none = f.readline().strip()
            key = f.readline().strip()
            iv = f.readline().strip()
            key = base64.b64decode(key)
            iv = base64.b64decode(iv)
        if len(key) != 32 or len(iv) != 16:
            return ValueError("Key or IV is not valid!")
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        with open(encrypt_file, 'rb') as f:
            ciphertext = f.read()
        unpadder = padding.PKCS7(128).unpadder()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        return unpadder.update(padded_data) + unpadder.finalize()

    @staticmethod
    def gen_ecc_key():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return public_key, private_key

    @staticmethod
    def ecc_encrypt(pub_key, file_path):
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        encrypted = pub_key.encrypt(
            plaintext,
            pad.OAEP(
                mgf=pad.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    @staticmethod
    def ecc_decrypt(key_file, encrypt_file):
        with open(key_file, 'rb') as f:
            lines = f.readlines()
        start = lines.index(b'-----BEGIN PRIVATE KEY-----\n')
        end = lines.index(b'-----END PRIVATE KEY-----\n')
        private_key = b''.join(lines[start:end + 1])
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )
        with open(encrypt_file, 'rb') as f:
            ciphertext = f.read()

        original = private_key.decrypt(
            ciphertext,
            pad.OAEP(
                mgf=pad.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return original

    @staticmethod
    def get_file_hash(path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f'File {path} does not exist')
        hasher = hashlib.md5()
        with open(path, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return hasher.hexdigest()
