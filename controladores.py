# controladores.py - Módulo de controladores para la gestión de mascotas, veterinarios y reservas en una veterinaria.
# Descripción: Este módulo contiene funciones para registrar, listar, eliminar y actualizar mascotas y veterinarios,
# así como para gestionar reservas de citas en una veterinaria. Utiliza SQLite para la persistencia de datos y maneja errores comunes de la base de datos.
# Requiere: sg_veterinaria.py, sg_hash.py
# Importaciones:
import sqlite3
from sg_veterinaria import *
from sg_hash import * 
from typing import Optional

# -----------------------------------------
# Registrar nueva mascota
# Inserta una mascota en la tabla 'mascotas' validando integridad y errores comunes.
# -----------------------------------------
def registrar_nueva_mascota(nombre: str, especie: str, raza: str, edad: int, peso: float, propietario_id: int) -> None:
    # Comienzo del try-except
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
            "INSERT INTO mascotas (nombre, especie, raza, edad, peso, propietario_id) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, especie, raza, edad, peso, propietario_id)
            )
            conn.commit() # Guardar los cambios, fin de las interacciones de sqlite3
            print(f"\n Mascota '{nombre}' agregada correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
        # Fin de la funcion, se organiza en bloques try-except para manejo de errores

# -----------------------------------------
# Listar mascotas
# Recupera e imprime todas las mascotas registradas en la base de datos.
# -----------------------------------------
def listar_mascotas() -> None:
    # Comienzo del try-except
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas")
            mascotas = cursor.fetchall()
            if not mascotas:
                print("\n No hay mascotas registradas.")
                return # Si no hay mascotas, se informa y se sale de la función
            print("\n Lista de Mascotas:")
            print("-" * 80)
            for mascota in mascotas: # Itera sobre cada mascota y la imprime en formato legible
                print(f"ID: {mascota[0]}, Nombre: {mascota[1]}, Especie: {mascota[2]}, Raza: {mascota[3]}, Edad: {mascota[4]}, Peso: {mascota[5]}, Propietario ID: {mascota[6]}")
            print("-" * 80)
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
        # Fin del try-except, sE maneja errores comunes de sqlite3

# -----------------------------------------
# Eliminar mascota
# Elimina una mascota específica usando su ID.
# -----------------------------------------
def eliminar_mascota(mascota_id: int) -> None:
     # Comienzo del try-except
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mascotas WHERE id = ?", (mascota_id,))
            if cursor.rowcount == 0:
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
            else:
                conn.commit() # Guardar los cambios y fin de las interacciones de sqlite3
                print(f"\n Mascota con ID {mascota_id} eliminada correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
        # Fin del try-except, se maneja errores comunes de sqlite3

# -----------------------------------------
# Actualizar mascota
# Modifica campos existentes de una mascota, manteniendo los actuales si no se pasan nuevos valores.
# -----------------------------------------
def actualizar_mascota(mascota_id: int, nombre: Optional[str]= None, especie: Optional[str] = None, raza: Optional[str] = None, edad: Optional[int] = None, peso: Optional[float] = None, propietario_id: Optional[int] = None) -> None:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mascotas WHERE id = ?", (mascota_id,))
            mascota = cursor.fetchone() # Obtener los datos actuales de la mascota, si existe
            if not mascota: # Si no existe la mascota, se informa y se sale de la función
                print(f"\n No se encontró ninguna mascota con ID {mascota_id}.")
                return
            nuevo_nombre = nombre if nombre is not None else mascota[1] # Mantener el valor actual si no se proporciona uno nuevo
            nueva_especie = especie if especie is not None else mascota[2] # Mantener el valor actual si no se proporciona uno nuevo
            nueva_raza = raza if raza is not None else mascota[3] # Mantener el valor actual si no se proporciona uno nuevo
            nueva_edad = edad if edad is not None else mascota[4] #...
            nuevo_peso = peso if peso is not None else mascota[5] #...
            nuevo_propietario_id = propietario_id if propietario_id is not None else mascota[6] #...
            cursor.execute(
                "UPDATE mascotas SET nombre = ?, especie = ?, raza = ?, edad = ?, peso = ?, propietario_id = ? WHERE id = ?",
                (nuevo_nombre, nueva_especie, nueva_raza, nueva_edad, nuevo_peso, nuevo_propietario_id, mascota_id)
            )
            conn.commit()
            print(f"\n Mascota con ID {mascota_id} actualizada correctamente.")# Fin de la función y de las interacciones de sqlite3

# -----------------------------------------
# Buscar mascotas por propietario
# Muestra todas las mascotas asociadas a un ID de propietario.
# -----------------------------------------
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

# -----------------------------------------
# Buscar mascotas por especie
# Filtra y muestra mascotas por tipo de especie.
# -----------------------------------------
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

# -----------------------------------------
# Contar mascotas
# Calcula el total de mascotas registradas.
# -----------------------------------------
def contar_mascotas() -> None:
    # Comienzo del try-except
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mascotas")
            count = cursor.fetchone()[0] # Obtener el conteo desde el resultado de la consulta
             # Imprimir el total de mascotas registradas
            print(f"\n Total de mascotas registradas: {count}")
    except sqlite3.IntegrityError as e:
        print(f"\n Error de integridad (posible duplicado o constraint):", e)
    except sqlite3.OperationalError as e:
        print(f"\n Error operacional (consulta mal escrita o BD inaccesible):", e)
    except sqlite3.DatabaseError as e:
        print(f"\n Error general de base de datos:", e)
        # Fin del try-except, se maneja errores comunes de sqlite3

# -----------------------------------------
# Crear reserva
# Inserta una nueva reserva de atención veterinaria.
# -----------------------------------------
def crear_reserva(idUsuario: int, idMascota: int, idVeterinario: int, fecha: str, hora: str, motivo: str, estadoMascota: str) -> None:
    #Cominzo del try-except
    try: 
        with conectar() as conn: # Conexión a la base de datos
            c = conn.cursor()
            c.execute(
                """
                INSERT INTO reservas (idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota)
            )
            conn.commit() # Guardar los cambios y fin de las interacciones de sqlite3
            print("Reserva creada exitosamente.") # Mensaje de éxito
    except sqlite3.DatabaseError as e:
        print("Error de base de datos inesperado: ", e )	  
    except Exception as e:
        print("Error inesperado: ", e)
        # Fin del try-except, se maneja errores comunes de sqlite3

# -----------------------------------------
# Mostrar reservas
# Lista todas las reservas almacenadas.
# -----------------------------------------
def mostrar_reservas() -> None:
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM reservas"
        )
        for fila in cursor.fetchall():
            print(f"ID Reserva: {fila[0]} , ID Usuario: {fila[1]}, ID Mascota: {fila[2]}, ID Veterinario: {fila[3]}, Fecha: {fila[4]}, Hora: {fila[5]}, Motivo: {fila[6]}, Estado Mascota: {fila[7]}")

# -----------------------------------------
# Modificar reserva
# Actualiza los campos de una reserva existente manteniendo los valores previos si se omiten.
# -----------------------------------------
def modificar_reserva(idReserva: int, idUsuario: Optional[int] = None, idMascota: Optional[int] = None, idVeterinario: Optional[int] = None, fecha: Optional[str] = None, hora: Optional[str] = None,
    motivo: Optional[str] = None, estadoMascota: Optional[str] = None) -> None:
    try: #Comienzo del try-except
        with conectar() as conn: # Conexión a la base de datos
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
    except Exception as e:
        print("Error inesperado: ", e)

# -----------------------------------------
# Eliminar reserva
# Borra una reserva por su ID.
# -----------------------------------------
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
    except Exception as e:
        print("Error inesperado: ", e)

# -----------------------------------------
# Registrar nuevo veterinario
# Inserta un veterinario con nombre y especialidad opcional.
# -----------------------------------------
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

# -----------------------------------------
# Listar veterinarios
# Muestra todos los veterinarios registrados.
# -----------------------------------------
def listar_veterinarios() -> None: 
     # Comienzo del try-except
    try:
        with conectar() as conn: # Conexión a la base de datos
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
        # Fin del try-except, se maneja errores comunes de sqlite3

# -----------------------------------------
# Eliminar veterinario
# Elimina un veterinario por ID y valida existencia por rowcount.
# -----------------------------------------
def eliminar_veterinario(veterinario_id: int) -> None: 
     # Comienzo del try-except
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM veterinarios WHERE idVeterinario = ?", (veterinario_id,))
            if cursor.rowcount == 0: # Si no se eliminó ninguna fila, el ID no existe,Se informa y se sale de la función
                #Se usa rowcount para verificar si se eliminó alguna fila
                print(f"\n No se encontró veterinario con ID {veterinario_id}.")
            else:
                conn.commit() # Guardar los cambios y fin de las interacciones de sqlite3
                print(f"\n Veterinario con ID {veterinario_id} eliminado correctamente.") #Mensaje de éxito
    except sqlite3.IntegrityError as e:
        print("\n Error de integridad:", e)
    except sqlite3.OperationalError as e:
        print("\n Error operacional:", e)
    except sqlite3.DatabaseError as e:
        print("\n Error general de base de datos:", e)
        # Fin del try-except, se maneja errores comunes de sqlite3

# -----------------------------------------
# Actualizar veterinario
# Modifica nombre y/o especialidad manteniendo valores actuales si no se envían nuevos.
# -----------------------------------------
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

# -----------------------------------------
# Buscar veterinarios por especialidad
# Filtra veterinarios por coincidencia exacta de especialidad.
# -----------------------------------------
def buscar_veterinarios_por_especialidad(especialidad: str) -> None:
    with conectar() as conn: # Conexión a la base de datos
        cursor = conn.cursor()
        cursor.execute(
            "SELECT idVeterinario, nombre, especialidad FROM veterinarios WHERE especialidad = ?",
            (especialidad,)
        )
        vets = cursor.fetchall() # Obtener todos los veterinarios que coincidan con la especialidad
         # Si no hay veterinarios con esa especialidad, se informa y se sale de la función
        if not vets:
            print(f"\n No hay veterinarios con especialidad '{especialidad}'.")
            return
        print(f"\n Veterinarios con especialidad '{especialidad}':") #Mensaje de exito 
        print("-" * 80)
        for v in vets:
            print(f"ID: {v[0]}, Nombre: {v[1]}") # Imprime ID y Nombre de cada veterinario encontrado
        print("-" * 80) 

# -----------------------------------------
# Buscar veterinarios por nombre
# Realiza búsqueda parcial usando LIKE y orden alfabético por nombre.
# -----------------------------------------
def buscar_veterinarios_por_nombre(texto: str) -> None:
    with conectar() as conn:
        cursor = conn.cursor()
        like = f"%{texto}%"
        cursor.execute(
            "SELECT idVeterinario, nombre, especialidad FROM veterinarios WHERE nombre LIKE ? ORDER BY nombre",
            (like,)
        ) # Usa LIKE para búsqueda parcial y ORDER BY para ordenar alfabéticamente el nombre
        vets = cursor.fetchall()
        if not vets:
            print(f"\n No hay veterinarios que coincidan con '{texto}'.") # Si no hay coincidencias, se informa y se sale de la función
            return
        print(f"\n Búsqueda por nombre contiene '{texto}':") #Mensaje de exito
        print("-" * 80)
        for v in vets:
            print(f"ID: {v[0]}, Nombre: {v[1]}, Especialidad: {v[2]}")
        print("-" * 80)

# -----------------------------------------
# Contar veterinarios
# Calcula el total de veterinarios registrados.
# -----------------------------------------
def contar_veterinarios() -> None:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM veterinarios")
            count = cursor.fetchone()[0]
            print(f"\n Total de veterinarios registrados: {count}") # Imprimir el total de veterinarios registrados

# -----------------------------------------
# Reporte: resumen general
# Muestra métricas generales: totales, edades y top de reservas por veterinario.
# -----------------------------------------
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

            print("\n=== REPORTE GENERAL DEL SISTEMA ===")
            print(f"Usuarios registrados:       {total_usuarios}")
            print(f"Veterinarios registrados:   {total_veterinarios}")
            print(f"Mascotas registradas:       {total_mascotas}")
            print(f"Reservas registradas:       {total_reservas}")
            print("-" * 60)
            print(f"Veterinario con más reservas: {vet_mas_reservas}")
            print(f"Edad mínima de mascotas:      {edad_min if edad_min else 'N/A'} años")
            print(f"Edad máxima de mascotas:      {edad_max if edad_max else 'N/A'} años")
            print(f"Edad promedio de mascotas:    {edad_promedio if edad_promedio else 'N/A'} años")
            print("-" * 60)
    except sqlite3.DatabaseError as e:
        print("Error de base de datos:", e)

# -----------------------------------------
# Exportar resumen general a TXT
# Genera un archivo de texto con las métricas del sistema.
# -----------------------------------------
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

        # Crear o sobrescribir el archivo
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("=== REPORTE GENERAL DEL SISTEMA ===\n\n")
            archivo.write(f"Usuarios registrados:       {total_usuarios}\n")
            archivo.write(f"Veterinarios registrados:   {total_veterinarios}\n")
            archivo.write(f"Mascotas registradas:       {total_mascotas}\n")
            archivo.write(f"Reservas registradas:       {total_reservas}\n")
            archivo.write("-" * 60 + "\n")
            archivo.write(f"Veterinario con más reservas: {vet_mas_reservas}\n")
            archivo.write(f"Edad mínima de mascotas:      {edad_min if edad_min else 'N/A'} años\n")
            archivo.write(f"Edad máxima de mascotas:      {edad_max if edad_max else 'N/A'} años\n")
            archivo.write(f"Edad promedio de mascotas:    {edad_promedio if edad_promedio else 'N/A'} años\n")
            archivo.write("-" * 60 + "\n")

        print(f"\nReporte exportado correctamente en: {ruta}")
    except sqlite3.DatabaseError as e:
        print("Error de base de datos:", e)
    except OSError as e:
        print("Error al escribir archivo:", e)

# -----------------------------------------
# Clase: Usuario
# Representa a un usuario del sistema.
# -----------------------------------------
class Usuario: 
    def __init__(self, idUsuario, nombre, email, password_hash, rol):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.rol = rol
        def __str__(self):
            return f"ID Usuario: {self.idUsuario}, Nombre: {self.nombre}, Email: {self.email}, Rol: {self.rol}" 

# -----------------------------------------
# Clase: Reserva
# Representa una reserva de atención veterinaria.
# -----------------------------------------
class Reserva:
    def __init__(self, idReserva, idUsuario, idMascota, idVeterinario, fecha, hora, motivo, estadoMascota):
        self.idReserva = idReserva
        self.idUsuario = idUsuario
        self.idMascota = idMascota
        self.idVeterinario = idVeterinario
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estadoMascota = estadoMascota
        def __str__(self):
            return f"ID Reserva: {self.idReserva}, Fecha: {self.fecha}, Hora: {self.hora}, Motivo: {self.motivo}, Estado de la Mascota: {self.estadoMascota}"

# -----------------------------------------
# Clase: Veterinario
# Representa a un veterinario con su especialidad.
# -----------------------------------------
class Veterinario: 
    def __init__(self, idVeterinario, nombre, especialidad):
        self.idVeterinario = idVeterinario
        self.nombre = nombre
        self.especialidad = especialidad
        def __str__(self):
            return f"ID Veterinario: {self.idVeterinario}, Nombre: {self.nombre}, Especialidad: {self.especialidad}"

# -----------------------------------------
# Clase: Mascota
# Representa a una mascota que será atendida.
# -----------------------------------------
class Mascota:
    def __init__(self, idMascota, idUsuario, nombre, especie, raza, edad):
        self.idMascota = idMascota
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        def __str__(self):
            return f"ID Mascota: {self.idMascota}, Nombre: {self.nombre}, Especie: {self.especie}, Raza: {self.raza}, Edad: {self.edad}"
