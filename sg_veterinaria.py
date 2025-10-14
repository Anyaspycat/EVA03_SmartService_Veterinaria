import sqlite3, os, hashlib, base64, hmac

DB_NAME = "sg_veterinaria.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def crear_tabla_usuarios():
    with conectar() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                rol TEXT NOT NULL
            )
            """
        )
        conn.commit()

def crear_tablas_veterinaria():
    with conectar() as conn:
        c = conn.cursor()
        c.execute(
            """ 
            CREATE TABLE IF NOT EXISTS veterinarios (
                idVeterinario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT
            )
            """
        )
        conn.commit()

def crear_tabla_mascotas():
    with conectar() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS mascotas (
                idMascota INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT,
                raza TEXT,
                edad INTEGER,
                idDueno INTEGER
            )
            """
        )
        conn.commit() 
        
def crear_tabla_reservas():
    with conectar() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS reservas (
                idReserva INTEGER PRIMARY KEY AUTOINCREMENT,
                idUsuario INTEGER,
                idMascota INTEGER,
                idVeterinario INTEGER,
                fecha DATE,
                hora TIME,
                motivo TEXT,
                estadoMascota TEXT,
                FOREIGN KEY (idMascota) REFERENCES mascotas(idMascota),
                FOREIGN KEY (idVeterinario) REFERENCES veterinarios(idVeterinario)
            )
            """
        )
        conn.commit()



