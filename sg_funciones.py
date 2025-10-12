import os, sqlite3, hashlib, hmac, base64
from sg_veterinaria import *
from sg_hash import * 

def registrar_login(username: str, email: str, password: str, rol: str) -> None:
    try:
        salt = os.urandom(SALT_LEN)
        hash = hash_password(password, salt)
        salt_b64 = base64.b64encode(salt).decode("utf-8")
        hash_b64 = base64.b64encode(hash).decode("utf-8")
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, password_salt, rol) VALUES (?, ?, ?, ?, ?)",
            (username, email, hash_b64, salt_b64, rol)
            )
            conn.commit()
            print(f"\n Usuario '{username}' agregado correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)

def verificar_login(username: str, password: str) -> bool:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "SELECT password_salt, password_hash FROM usuarios WHERE nombre = ?",
            (username,)
            )
            row = cursor.fetchone()
            if not row:
                return False
            salt_row = base64.b64decode(row[0])
            hash_row = base64.b64decode(row[1])
            hash_login = hash_password(password, salt_row)
            return hmac.compare_digest(hash_login, hash_row)
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
