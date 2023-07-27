from nacl.public import PrivateKey, SealedBox
from nacl.signing import SigningKey
from nacl.secret import SecretBox
from nacl.utils import random
from os.path import exists
from config import nacl_sk_path


if not exists(nacl_sk_path):
    sk = PrivateKey.generate()
    sk_raw = sk.encode()
    with open(nacl_sk_path, 'wb') as f:
        f.write(sk_raw)
else:
    with open(nacl_sk_path, 'rb') as f:
        sk_raw = f.read()
        


def encrypt(plaintext: bytes):
    return SealedBox(PrivateKey(sk_raw).public_key).encrypt(plaintext)


def decrypt(ciphertext: bytes):
    return SealedBox(PrivateKey(sk_raw)).decrypt(ciphertext)


def sign(message: bytes):
    return SigningKey(sk_raw).sign(message).signature


def verify(message: bytes, signature: bytes):
    return SigningKey(sk_raw).verify_key.verify(message, signature)


def new_symmetric_key():
    return random(SecretBox.KEY_SIZE)


def symmetric_encrypt(symmetric_key: bytes, plaintext: bytes):
    return SecretBox(symmetric_key).encrypt(plaintext)


def symmetric_decrypt(symmetric_key: bytes, ciphertext: bytes):
    return SecretBox(symmetric_key).decrypt(ciphertext)


def get_pk_raw():
    return PrivateKey(sk_raw).public_key.encode(),print(PrivateKey(sk_raw).public_key.encode())


def new_pair():
    sk = PrivateKey.generate()
    return sk.encode(), sk.public_key.encode()