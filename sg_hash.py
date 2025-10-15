import os, sqlite3, hashlib, hmac, base64
# Parametros para el scrypt
# Valores recomendados por OWASP (https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
# Ajustar segun las necesidades de seguridad y rendimiento
# A mayor N, mayor seguridad pero tambien mayor consumo de recursos
# R y P pueden ajustarse para optimizar el uso de memoria y CPU
# KEY_LEN es la longitud del hash resultante
# SALT_LEN es la longitud de la sal utilizada
# Valores por defecto: N=16384, R=8, P=1, KEY_LEN=32, SALT_LEN=16
# Estos valores son un buen compromiso entre seguridad y rendimiento para la mayoría de las aplicaciones
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
