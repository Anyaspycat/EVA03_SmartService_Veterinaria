import sqlite3
from sg_veterinaria import *
from sg_hash import * 
from typing import Optional

def registrar_nueva_mascota(nombre: str, especie: str, raza: str, edad: int, peso: float, propietario_id: int) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO mascotas (nombre, especie, raza, edad, peso, propietario_id) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, especie, raza, edad, peso, propietario_id)
            )
            conn.commit()
            print(f"\n Mascota '{nombre}' agregada correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
def listar_mascotas() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("\n No hay mascotas registradas.")
                return
            print("\n Lista de Mascotas:")
            print("-" * 80)
            for mascota in mascotas:
                print(f"ID: {mascota[0]}, Nombre: {mascota[1]}, Especie: {mascota[2]}, Raza: {mascota[3]}, Edad: {mascota[4]}, Peso: {mascota[5]}, Propietario ID: {mascota[6]}")
            print("-" * 80)
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
def eliminar_mascota(mascota_id: int) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            if cursor.rowcount == 0:
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
            else:
                conn.commit()
                print(f"\n Mascota con ID {mascota_id} eliminada correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
def actualizar_mascota(mascota_id: int, nombre: Optional[str]= None, especie: Optional[str] = None, raza: Optional[str] = None, edad: Optional[int] = None, peso: Optional[float] = None, propietario_id: Optional[int] = None) -> None:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE id = ?", (mascota_id,))
            mascota = cursor.fetchone()
            if not mascota:
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
                return
            nuevo_nombre = nombre if nombre is not None else mascota[1]
            nueva_especie = especie if especie is not None else mascota[2]
            nueva_raza = raza if raza is not None else mascota[3]
            nueva_edad = edad if edad is not None else mascota[4]
            nuevo_peso = peso if peso is not None else mascota[5]
            nuevo_propietario_id = propietario_id if propietario_id is not None else mascota[6]
            cursor.execute(
                "UPDATE mascotas SET nombre = ?, especie = ?, raza = ?, edad = ?, peso = ?, propietario_id = ? WHERE id = ?",
                (nuevo_nombre, nueva_especie, nueva_raza, nueva_edad, nuevo_peso, nuevo_propietario_id, mascota_id)
            )
            conn.commit()
            print(f"\n Mascota con ID {mascota_id} actualizada correctamente.")
def buscar_mascotas_por_propietario(propietario_id: int) -> None:
 
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE propietario_id = ?", (propietario_id,))
            mascotas = cursor.fetchall()
            if not mascotas:
                print(f"\n No hay mascotas registradas para el propietario con ID {propietario_id}.")
                return
            print(f"\n Mascotas del Propietario ID {propietario_id}:")
            print("-" * 80)
            for mascota in mascotas:
                print(f"ID: {mascota[0]}, Nombre: {mascota[1]}, Especie: {mascota[2]}, Raza: {mascota[3]}, Edad: {mascota[4]}, Peso: {mascota[5]}")
            print("-" * 80)
def buscar_mascotas_por_especie(especie: str) -> None: 

        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE especie = ?", (especie,))
            mascotas = cursor.fetchall()
            if not mascotas:
                print(f"\n No hay mascotas registradas de la especie '{especie}'.")
                return
            print(f"\n Mascotas de la Especie '{especie}':")
            print("-" * 80)
            for mascota in mascotas:
                print(f"ID: {mascota[0]}, Nombre: {mascota[1]}, Raza: {mascota[3]}, Edad: {mascota[4]}, Peso: {mascota[5]}, Propietario ID: {mascota[6]}")
            print("-" * 80)            
def contar_mascotas() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mascotas")
            count = cursor.fetchone()[0]
            print(f"\n Total de mascotas registradas: {count}")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)

#Crud Reserva
def crear_reserva(): 
    try: 
        with conectar() as conn:
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO reservas (idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota)
            )
            conn.commit()
            print("Reserva creada exitosamente.")

    except sqlite3.DatabaseError as e:
        print("Error de base de datos inesperado: ", e )
    except sqlite3.IntegrityError as e:
        print("Error de Integridad de datos: ", e)
    except Exception as e:
        print("Error inesperado: ", e)


def mostrar_reservas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reservas"
        )
        for fila in cursor.fetchall():
            print(f"ID Reserva: {fila[0]} , ID Usuario: {fila[1]}, ID Mascota: {fila[2]}, ID Veterinario: {fila[3]}, Fecha: {fila[4]}, Hora: {fila[5]}, Motivo: {fila[6]}, Estado Mascota: {fila[7]}")


def modificar_reserva():
    try:
        with conectar() as conn:
            c = conn.cursor()
            c.execute(
                """
                UPDATE reservas
                SET idUsuario = ?, idMascota = ?, idVeterinario = ?, fecha = ?, hora = ?, motivo = ?, estadoMascota = ?
                WHERE idReserva = ?
                """,
                (idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota, idReserva)
            )
            conn.commit()
            if c.rowcount == 0:
                print("No se encontró la reserva con el ID proporcionado.")
            else:
                print("Reserva modificada exitosamente.")

    except sqlite3.DatabaseError as e:
        print("Error de base de datos inesperado: ", e )
    except sqlite3.IntegrityError as e:
        print("Error de Integridad de datos: ", e)
    except Exception as e:
        print("Error inesperado: ", e)


def eliminar_reserva():
    try:
        with conectar() as conn:
            c = conn.cursor()
            c.execute(
                """
                DELETE FROM reservas
                WHERE idReserva = ?
                """,
                (idReserva, )
            )
            conn.commit()
            if c.rowcount == 0:
                print("No se encontró la reserva con el ID proporcionado.")
            else:
                print("Reserva eliminada exitosamente.")

    except sqlite3.DatabaseError as e:
        print("Error de base de datos inesperado: ", e )
    except sqlite3.IntegrityError as e:
        print("Error de Integridad de datos: ", e)
    except Exception as e:
        print("Error inesperado: ", e)


