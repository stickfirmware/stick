import hashlib
import binascii
import os

def hash_pin(pin, rounds=1000):
    salt = os.urandom(32)
    h = hashlib.sha256(salt + pin.encode())
    for _ in range(rounds):
        h = hashlib.sha256(h.digest())
    hash_hex = binascii.hexlify(h.digest()).decode()
    salt_hex = binascii.hexlify(salt).decode()
    return hash_hex, salt_hex

def verify_pin(pin, salt_hex, hash_hex, rounds=1000):
    salt = binascii.unhexlify(salt_hex)
    h = hashlib.sha256(salt + pin.encode())
    for _ in range(rounds):
        h = hashlib.sha256(h.digest())
    return binascii.hexlify(h.digest()).decode() == hash_hex