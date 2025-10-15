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

def crear_reserva(idUsuario: int, idMascota: int, idVeterinario: int, fecha: str, hora: str, motivo: str, estadoMascota: str) -> None:
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

def mostrar_reservas() -> None:
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reservas"
        )
        for fila in cursor.fetchall():
            print(f"ID Reserva: {fila[0]} , ID Usuario: {fila[1]}, ID Mascota: {fila[2]}, ID Veterinario: {fila[3]}, Fecha: {fila[4]}, Hora: {fila[5]}, Motivo: {fila[6]}, Estado Mascota: {fila[7]}")

def modificar_reserva(idReserva: int, idUsuario: Optional[int] = None, idMascota: Optional[int] = None, idVeterinario: Optional[int] = None, fecha: Optional[str] = None, hora: Optional[str] = None,
    motivo: Optional[str] = None, estadoMascota: Optional[str] = None) -> None:
    try:
        with conectar() as conn:
            c = conn.cursor()
            # Trae valores actuales
            c.execute(
                """SELECT idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota
                   FROM reservas WHERE idReserva = ?""",
                (idReserva,)
            )
            r = c.fetchone()
            if not r:
                print(f"\n No se encontró la reserva con ID {idReserva}.")
                return
            # Mantén lo existente si viene None
            nuevo_idUsuario     = idUsuario     if idUsuario     is not None else r[0]
            nuevo_idMascota     = idMascota     if idMascota     is not None else r[1]
            nuevo_idVeterinario = idVeterinario if idVeterinario is not None else r[2]
            nueva_fecha         = fecha if fecha is not None else r[3]
            nueva_hora          = hora  if hora  is not None else r[4]
            nuevo_motivo        = motivo        if motivo        is not None else r[5]
            nuevo_estado        = estadoMascota if estadoMascota is not None else r[6]
            c.execute(
                """UPDATE reservas
                   SET idUsuario = ?, idMascota = ?, idVeterinario = ?, fecha = ?, hora = ?, motivo = ?, estadoMascota = ?
                   WHERE idReserva = ?""",
                (nuevo_idUsuario, nuevo_idMascota, nuevo_idVeterinario,
                 nueva_fecha, nueva_hora, nuevo_motivo, nuevo_estado, idReserva)
            )
            conn.commit()
            if c.rowcount == 0:
                print("\n No se actualizó ninguna fila.")
            else:
                print("\n Reserva actualizada correctamente.")
    except sqlite3.DatabaseError as e:
        print("Error de base de datos inesperado: ", e )
    except sqlite3.IntegrityError as e:
        print("Error de Integridad de datos: ", e)
    except Exception as e:
        print("Error inesperado: ", e)

def eliminar_reserva(idReserva: int) -> None:
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

def registrar_nuevo_veterinario(nombre: str, especialidad: Optional[str] = None) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO veterinarios (nombre, especialidad) VALUES (?, ?)",
                (nombre, especialidad)
            )
            conn.commit()
            print(f"\n Veterinario '{nombre}' agregado correctamente.")
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)

def listar_veterinarios() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT idVeterinario, nombre, especialidad FROM veterinarios")
            vets = cursor.fetchall()
            if not vets:
                print("\n No hay veterinarios registrados.")
                return
            print("\n Lista de Veterinarios:")
            print("-" * 80)
            for v in vets:
                print(f"ID: {v[0]}, Nombre: {v[1]}, Especialidad: {v[2]}")
            print("-" * 80)
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)

def eliminar_veterinario(veterinario_id: int) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM veterinarios WHERE idVeterinario = ?", (veterinario_id,))
            if cursor.rowcount == 0:
                print(f"\n No se encontró veterinario con ID {veterinario_id}.")
            else:
                conn.commit()
                print(f"\n Veterinario con ID {veterinario_id} eliminado correctamente.")
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)

def actualizar_veterinario(veterinario_id: int, nombre: Optional[str] = None, especialidad: Optional[str] = None) -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT idVeterinario, nombre, especialidad FROM veterinarios WHERE idVeterinario = ?",
                (veterinario_id,)
            )
            v = cursor.fetchone()
            if not v:
                print(f"\n No se encontró veterinario con ID {veterinario_id}.")
                return
            nuevo_nombre = nombre if nombre is not None else v[1]
            nueva_especialidad = especialidad if especialidad is not None else v[2]
            cursor.execute(
                "UPDATE veterinarios SET nombre = ?, especialidad = ? WHERE idVeterinario = ?",
                (nuevo_nombre, nueva_especialidad, veterinario_id)
            )
            conn.commit()
            print(f"\n Veterinario con ID {veterinario_id} actualizado correctamente.")
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)

def buscar_veterinarios_por_especialidad(especialidad: str) -> None:
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idVeterinario, nombre, especialidad FROM veterinarios WHERE especialidad = ?",
            (especialidad,)
        )
        vets = cursor.fetchall()
        if not vets:
            print(f"\n No hay veterinarios con especialidad '{especialidad}'.")
            return
        print(f"\n Veterinarios con especialidad '{especialidad}':")
        print("-" * 80)
        for v in vets:
            print(f"ID: {v[0]}, Nombre: {v[1]}")
        print("-" * 80)

def buscar_veterinarios_por_nombre(texto: str) -> None:
    with conectar() as conn:
        cursor = conn.cursor()
        like = f"%{texto}%"
        cursor.execute(
            "SELECT idVeterinario, nombre, especialidad FROM veterinarios WHERE nombre LIKE ? ORDER BY nombre",
            (like,)
        )
        vets = cursor.fetchall()
        if not vets:
            print(f"\n No hay veterinarios que coincidan con '{texto}'.")
            return
        print(f"\n Búsqueda por nombre contiene '{texto}':")
        print("-" * 80)
        for v in vets:
            print(f"ID: {v[0]}, Nombre: {v[1]}, Especialidad: {v[2]}")
        print("-" * 80)

def contar_veterinarios() -> None:
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM veterinarios")
            count = cursor.fetchone()[0]
            print(f"\n Total de veterinarios registrados: {count}")
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)

def reporte_resumen_general() -> None:
    try:
        with conectar() as conn:
            c = conn.cursor()

            # Conteos generales
            c.execute("SELECT COUNT(*) FROM usuarios"); total_usuarios = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM veterinarios"); total_veterinarios = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM mascotas"); total_mascotas = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM reservas"); total_reservas = c.fetchone()[0]

            # Mascota más joven y más vieja
            c.execute("SELECT MIN(edad), MAX(edad) FROM mascotas")
            edad_min, edad_max = c.fetchone()

            # Promedio de edad de las mascotas
            c.execute("SELECT ROUND(AVG(edad), 1) FROM mascotas WHERE edad IS NOT NULL")
            edad_promedio = c.fetchone()[0]

            # Veterinario con más reservas
            c.execute("""
                SELECT v.nombre, COUNT(r.idReserva) AS total
                FROM veterinarios v
                LEFT JOIN reservas r ON v.idVeterinario = r.idVeterinario
                GROUP BY v.idVeterinario
                ORDER BY total DESC
                LIMIT 1
            """)
            top_vet = c.fetchone()
            vet_mas_reservas = f"{top_vet[0]} ({top_vet[1]} reservas)" if top_vet and top_vet[1] > 0 else "Sin registros"

            # Usuario con más mascotas registradas
            c.execute("""
                SELECT u.nombre, COUNT(m.idMascota) AS total
                FROM usuarios u
                LEFT JOIN mascotas m ON u.idUsuario = m.idDueno
                GROUP BY u.idUsuario
                ORDER BY total DESC
                LIMIT 1
            """)
            top_usuario = c.fetchone()
            usuario_mas_mascotas = f"{top_usuario[0]} ({top_usuario[1]} mascotas)" if top_usuario and top_usuario[1] > 0 else "Sin registros"

            print("\n=== REPORTE GENERAL DEL SISTEMA ===")
            print(f"Usuarios registrados:       {total_usuarios}")
            print(f"Veterinarios registrados:   {total_veterinarios}")
            print(f"Mascotas registradas:       {total_mascotas}")
            print(f"Reservas registradas:       {total_reservas}")
            print("-" * 60)
            print(f"Veterinario con más reservas: {vet_mas_reservas}")
            print(f"Usuario con más mascotas:     {usuario_mas_mascotas}")
            print(f"Edad mínima de mascotas:      {edad_min if edad_min else 'N/A'} años")
            print(f"Edad máxima de mascotas:      {edad_max if edad_max else 'N/A'} años")
            print(f"Edad promedio de mascotas:    {edad_promedio if edad_promedio else 'N/A'} años")
            print("-" * 60)

    except sqlite3.DatabaseError as e:
        print("Error de base de datos:", e)

def exportar_resumen_general_txt(ruta: str = "reporte_resumen_general.txt") -> None:
    try:
        with conectar() as conn:
            c = conn.cursor()

            # Conteos generales
            c.execute("SELECT COUNT(*) FROM usuarios"); total_usuarios = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM veterinarios"); total_veterinarios = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM mascotas"); total_mascotas = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM reservas"); total_reservas = c.fetchone()[0]

            # Mascota más joven y más vieja
            c.execute("SELECT MIN(edad), MAX(edad) FROM mascotas")
            edad_min, edad_max = c.fetchone()

            # Promedio de edad de las mascotas
            c.execute("SELECT ROUND(AVG(edad), 1) FROM mascotas WHERE edad IS NOT NULL")
            edad_promedio = c.fetchone()[0]

            # Veterinario con más reservas
            c.execute("""
                SELECT v.nombre, COUNT(r.idReserva) AS total
                FROM veterinarios v
                LEFT JOIN reservas r ON v.idVeterinario = r.idVeterinario
                GROUP BY v.idVeterinario
                ORDER BY total DESC
                LIMIT 1
            """)
            top_vet = c.fetchone()
            vet_mas_reservas = f"{top_vet[0]} ({top_vet[1]} reservas)" if top_vet and top_vet[1] > 0 else "Sin registros"

            # Usuario con más mascotas registradas
            c.execute("""
                SELECT u.nombre, COUNT(m.idMascota) AS total
                FROM usuarios u
                LEFT JOIN mascotas m ON u.idUsuario = m.idDueno
                GROUP BY u.idUsuario
                ORDER BY total DESC
                LIMIT 1
            """)
            top_usuario = c.fetchone()
            usuario_mas_mascotas = f"{top_usuario[0]} ({top_usuario[1]} mascotas)" if top_usuario and top_usuario[1] > 0 else "Sin registros"

        # Crear o sobrescribir el archivo
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("=== REPORTE GENERAL DEL SISTEMA ===\n\n")
            archivo.write(f"Usuarios registrados:       {total_usuarios}\n")
            archivo.write(f"Veterinarios registrados:   {total_veterinarios}\n")
            archivo.write(f"Mascotas registradas:       {total_mascotas}\n")
            archivo.write(f"Reservas registradas:       {total_reservas}\n")
            archivo.write("-" * 60 + "\n")
            archivo.write(f"Veterinario con más reservas: {vet_mas_reservas}\n")
            archivo.write(f"Usuario con más mascotas:     {usuario_mas_mascotas}\n")
            archivo.write(f"Edad mínima de mascotas:      {edad_min if edad_min else 'N/A'} años\n")
            archivo.write(f"Edad máxima de mascotas:      {edad_max if edad_max else 'N/A'} años\n")
            archivo.write(f"Edad promedio de mascotas:    {edad_promedio if edad_promedio else 'N/A'} años\n")
            archivo.write("-" * 60 + "\n")

        print(f"\nReporte exportado correctamente en: {ruta}")

    except sqlite3.DatabaseError as e:
        print("Error de base de datos:", e)
    except OSError as e:
        print("Error al escribir archivo:", e)



class Usuario: 


