import os, sqlite3, hashlib, hmac, base64

SCRYPT_N = 2**14       
SCRYPT_R = 8           
SCRYPT_P = 1            
KEY_LEN = 32  
SALT_LEN = 16 

def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password = password.encode("utf-8"),
        salt = salt,
        n = SCRYPT_N,
        r = SCRYPT_R,
        p = SCRYPT_P,
        dklen = KEY_LEN
    )
