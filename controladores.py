import sqlite3, os, hashlib, base64, hmac 
from sg_veterinaria import *
from sg_hash import * 

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
def actualizar_mascota(mascota_id: int, nombre: str = None, especie: str = None, raza: str = None, edad: int = None, peso: float = None, propietario_id: int = None) -> None:
    try:
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
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
def buscar_mascotas_por_propietario(propietario_id: int) -> None:
    try:
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
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
def buscar_mascotas_por_especie(especie: str) -> None: 
    try:
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
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e
              
              
              
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
        
        
def listar_mascotas_ordenadas_por_nombre() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas ORDER BY nombre ASC")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("\n No hay mascotas registradas.")
                return
            print("\n Lista de Mascotas Ordenadas por Nombre:")
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
        
def listar_mascotas_ordenadas_por_edad() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas ORDER BY edad ASC")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("\n No hay mascotas registradas.")
                return
            print("\n Lista de Mascotas Ordenadas por Edad:")
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
        
def listar_mascotas_ordenadas_por_peso() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas ORDER BY peso ASC")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("\n No hay mascotas registradas.")
                return
            print("\n Lista de Mascotas Ordenadas por Peso:")
            print("-" * 80)
            for mascota in mascotas:
                print(f"ID: {mascota[0]}, Nombre: {mascota[1]}, Especie: {mascota[2]}, Raza: {mascota[3]}, Edad: {mascota[4]}, Peso: {mascota[5]}, Propietario ID: {mascota[6]}")
            print("-" * 80)
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e
def editar_mascota_interactivo() -> None:
    try:
        mascota_id = int(input("\n Ingrese el ID de la mascota a editar: "))
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE id = ?", (mascota_id,))
            mascota = cursor.fetchone()
            if not mascota:
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
                return
            print(f"\n Editando Mascota ID {mascota_id}. Presione Enter para mantener el valor actual.")
            nuevo_nombre = input(f"Nombre ({mascota[1]}): ") or mascota[1]
            nueva_especie = input(f"Especie ({mascota[2]}): ") or mascota[2]
            nueva_raza = input(f"Raza ({mascota[3]}): ") or mascota[3]
            nueva_edad_input = input(f"Edad ({mascota[4]}): ")
            nueva_edad = int(nueva_edad_input) if nueva_edad_input else mascota[4]
            nuevo_peso_input = input(f"Peso ({mascota[5]}): ")
            nuevo_peso = float(nuevo_peso_input) if nuevo_peso_input else mascota[5]
            nuevo_propietario_id_input = input(f"Propietario ID ({mascota[6]}): ")
            nuevo_propietario_id = int(nuevo_propietario_id_input) if nuevo_propietario_id_input else mascota[6]
            cursor.execute(
                "UPDATE mascotas SET nombre = ?, especie = ?, raza = ?, edad = ?, peso = ?, propietario_id = ? WHERE id = ?",
                (nuevo_nombre, nueva_especie, nueva_raza, nueva_edad, nuevo_peso, nuevo_propietario_id, mascota_id)
            )
            conn.commit()
            print(f"\n Mascota con ID {mascota_id} actualizada correctamente.")
    except ValueError:
        print("\n Entrada inválida. Asegúrese de ingresar números para ID, Edad, Peso y Propietario ID.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
        
def eliminar_mascota_interactivo() -> None:
    try:
        mascota_id = int(input("\n Ingrese el ID de la mascota a eliminar: "))
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            if cursor.rowcount == 0:
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
            else:
                conn.commit()
                print(f"\n Mascota con ID {mascota_id} eliminada correctamente.")
    except ValueError:
        print("\n Entrada inválida. Asegúrese de ingresar un número para el ID.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
