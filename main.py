# main.py
# Trabajo Práctico N°3 - Programación Segura
# Descripción general:
# Programa principal que maneja el flujo de la aplicación de gestión de veterinaria.
# Permite a los usuarios registrarse, iniciar sesión y acceder a un menú principal con opciones
# para gestionar veterinarios, mascotas y reservas, utilizando funciones definidas en otros módulos.

# Importación de módulos principales y funciones auxiliares
# Cada módulo encapsula la lógica de una parte del sistema:
# - sg_veterinaria: funciones CRUD de veterinarios y mascotas
# - sg_funciones: utilidades generales, manejo de DB y autenticación
# - controladores: capa intermedia de validación y conexión entre UI y lógica
import sqlite3
from sg_veterinaria import *
from sg_funciones import *
from controladores import *

# ---------------------------------------------------------------------------------
# Inicialización de la base de datos
# Se crean las tablas en SQLite solo si no existen para garantizar la persistencia.
# Esto permite ejecutar el programa sin pasos manuales previos de migración.
# ---------------------------------------------------------------------------------
crear_tabla_usuarios()       # Crear tabla usuarios si no existe
crear_tablas_veterinaria()   # Crear tabla veterinarios si no existe
crear_tabla_mascotas()       # Crear tabla mascotas si no existe
crear_tabla_reservas()       # Crear tabla reservas si no existe

# -----------------------------------------
# Menú de Veterinarios
# Permite registrar, listar, actualizar, eliminar y buscar veterinarios.
# También incluye utilidades de conteo y filtros por nombre/especialidad.
# -----------------------------------------
def menu_veterinarios():
    while True:
        print("\n--- Veterinarios ---")
        print("1.- Registrar nuevo")
        print("2.- Listar")
        print("3.- Actualizar")
        print("4.- Eliminar")
        print("5.- Buscar por nombre")
        print("6.- Buscar por especialidad")
        print("7.- Contar veterinarios")
        print("8.- Volver\n")

        opcion = input("Favor ingresar opción: ").strip().lower()

        if opcion == '1':
            # Entrada libre de texto. La especialidad es opcional.
            nombre_veterinario = input("Nombre: ").strip()
            especialidad_veterinario = input("Especialidad (opcional): ").strip() or None
            registrar_nuevo_veterinario(nombre_veterinario, especialidad_veterinario)
        elif opcion == '2':
            listar_veterinarios()
        elif opcion == '3':
            # Se valida que el ID sea numérico antes de actualizar.
            try:
                id_veterinario = int(input("ID del veterinario: "))
            except ValueError:
                print("ID inválido."); continue
            # Si el usuario presiona Enter, se conserva el valor anterior mediante None.
            nuevo_nombre = input("Nuevo nombre (Enter mantiene): ").strip()
            nueva_especialidad = input("Nueva especialidad (Enter mantiene): ").strip()
            actualizar_veterinario(
                id_veterinario,
                nuevo_nombre if nuevo_nombre else None,
                nueva_especialidad if nueva_especialidad else None
            )
        elif opcion == '4':
            # Validación de ID numérico para eliminación.
            try:
                id_veterinario = int(input("ID del veterinario: "))
            except ValueError:
                print("ID inválido."); continue
            eliminar_veterinario(id_veterinario)
        elif opcion == '5':
            texto_nombre = input("Nombre contiene: ").strip()
            buscar_veterinarios_por_nombre(texto_nombre)
        elif opcion == '6':
            especialidad = input("Especialidad exacta: ").strip()
            buscar_veterinarios_por_especialidad(especialidad)
        elif opcion == '7':
            contar_veterinarios()
        elif opcion == '8':
            break
        else:
            print("Favor ingresar una de las opciones válidas\n")

# -----------------------------------------
# Menú de Mascotas
# Permite CRUD de mascotas y consultas por propietario o especie.
# Incluye validación de tipos para edad, peso e IDs relacionados.
# -----------------------------------------
def menu_mascotas():
    while True:
        print("\n--- Mascotas ---")
        print("1.- Registrar nueva")
        print("2.- Listar")
        print("3.- Actualizar")
        print("4.- Eliminar")
        print("5.- Buscar por propietario")
        print("6.- Buscar por especie")
        print("7.- Contar")
        print("8.- Volver\n")
        opcion = input("Favor ingresar opción: ").strip().lower()

        if opcion == '1':
            # Registro con validación de tipos básicos. Puede lanzar ValueError si no es numérico.
            nombre = input("Nombre: ").strip()
            especie = input("Especie: ").strip()
            raza = input("Raza: ").strip()
            edad = int(input("Edad: ").strip())
            peso = float(input("Peso: ").strip())
            propietario_id = int(input("ID propietario: ").strip())
            registrar_nueva_mascota(nombre, especie, raza, edad, peso, propietario_id)
        elif opcion == '2':
            listar_mascotas()
        elif opcion == '3':
            # Validación de ID de la mascota a actualizar.
            try:
                id_mascota = int(input("ID mascota: "))
            except ValueError:
                print("ID inválido."); continue
            # Campos opcionales: Enter conserva valor previo (se envía None).
            nombre = input("Nuevo nombre (Enter mantiene): ").strip()
            especie = input("Nueva especie (Enter mantiene): ").strip()
            raza = input("Nueva raza (Enter mantiene): ").strip()
            edad_txt = input("Nueva edad (Enter mantiene): ").strip()
            peso_txt = input("Nuevo peso (Enter mantiene): ").strip()
            dueno_txt = input("Nuevo ID propietario (Enter mantiene): ").strip()
            actualizar_mascota(
                id_mascota,
                nombre or None,
                especie or None,
                raza or None,
                int(edad_txt) if edad_txt else None,
                float(peso_txt) if peso_txt else None,
                int(dueno_txt) if dueno_txt else None
            )
        elif opcion == '4':
            try:
                id_mascota = int(input("ID mascota: "))
            except ValueError:
                print("ID inválido."); continue
            eliminar_mascota(id_mascota)
        elif opcion == '5':
            try:
                id_propietario = int(input("ID propietario: "))
            except ValueError:
                print("ID inválido."); continue
            buscar_mascotas_por_propietario(id_propietario)
        elif opcion == '6':
            especie = input("Especie: ").strip()
            buscar_mascotas_por_especie(especie)
        elif opcion == '7':
            contar_mascotas()
        elif opcion == '8':
            break
        else:
            print("Favor ingresar una de las opciones válidas\n")

# -----------------------------------------
# Menú de Reservas
# Gestiona creación, visualización, modificación y eliminación de reservas.
# Valida IDs y permite actualizaciones parciales manteniendo valores previos con None.
# -----------------------------------------
def menu_reservas():
    while True:
        print("\n--- Reservas ---")
        print("1.- Crear nueva reserva")
        print("2.- Mostrar todas las reservas")
        print("3.- Modificar una reserva")
        print("4.- Eliminar una reserva")
        print("5.- Volver\n")

        opcion_menu = input("Elige una opción: ").strip().lower()

        if opcion_menu == '1':
            # Validación de IDs numéricos para relaciones foráneas.
            try:
                id_usuario = int(input("ID del usuario: ").strip())
                id_mascota = int(input("ID de la mascota: ").strip())
                id_veterinario = int(input("ID del veterinario: ").strip())
            except ValueError:
                print("Algún ID no es numérico."); continue

            # Formatos de fecha y hora esperados: YYYY-MM-DD y HH:MM:SS
            fecha_reserva = input("Fecha (YYYY-MM-DD): ").strip()
            hora_reserva = input("Hora (HH:MM:SS): ").strip()
            motivo_reserva = input("Motivo de la reserva: ").strip()
            estado_mascota = input("Estado de la mascota: ").strip()

            crear_reserva(
                id_usuario,
                id_mascota,
                id_veterinario,
                fecha_reserva,
                hora_reserva,
                motivo_reserva,
                estado_mascota
            )

        elif opcion_menu == '2':
            mostrar_reservas()

        elif opcion_menu == '3':
            # Se valida ID numérico de la reserva a modificar.
            try:
                id_reserva = int(input("ID de la reserva a modificar: ").strip())
            except ValueError:
                print("El ID de la reserva debe ser numérico."); continue

            # Entradas opcionales: si el usuario presiona Enter se envía None para conservar.
            texto_id_usuario = input("Nuevo ID de usuario (Enter mantiene): ").strip()
            texto_id_mascota = input("Nuevo ID de mascota (Enter mantiene): ").strip()
            texto_id_veterinario = input("Nuevo ID de veterinario (Enter mantiene): ").strip()
            nueva_fecha = input("Nueva fecha (YYYY-MM-DD, Enter mantiene): ").strip()
            nueva_hora = input("Nueva hora (HH:MM:SS, Enter mantiene): ").strip()
            nuevo_motivo = input("Nuevo motivo (Enter mantiene): ").strip()
            nuevo_estado = input("Nuevo estado (Enter mantiene): ").strip()

            nuevo_id_usuario = int(texto_id_usuario) if texto_id_usuario else None
            nuevo_id_mascota = int(texto_id_mascota) if texto_id_mascota else None
            nuevo_id_veterinario = int(texto_id_veterinario) if texto_id_veterinario else None

            modificar_reserva(
                id_reserva,
                nuevo_id_usuario,
                nuevo_id_mascota,
                nuevo_id_veterinario,
                nueva_fecha or None,
                nueva_hora or None,
                nuevo_motivo or None,
                nuevo_estado or None
            )

        elif opcion_menu == '4':
            try:
                id_reserva = int(input("ID de la reserva a eliminar: ").strip())
            except ValueError:
                print("El ID de la reserva debe ser numérico."); continue
            eliminar_reserva(id_reserva)

        elif opcion_menu == '5':
            break
        else:
            print("Opción no válida. Intenta nuevamente.")

# -----------------------------------------
# Menú de Reportes
# Opción 1: muestra en pantalla el resumen general (conteos por entidad).
# Opción 2: exporta el mismo resumen a un archivo .txt en la ruta indicada.
# -----------------------------------------
def menu_reportes():
    while True:
        print("\n--- Reportes ---")
        print("1.- Resumen general en pantalla")
        print("2.- Exportar resumen general a TXT")
        print("3.- Volver\n")
        opcion = input("Favor ingresar opción: ").strip().lower()

        if opcion == '1':
            # Muestra métricas generales útiles para entrega y verificación rápida.
            reporte_resumen_general()
        elif opcion == '2':
            # Exporta el reporte a texto plano. Si se deja vacío, usa un nombre por defecto.
            ruta_archivo = input("Ruta del archivo (Enter por defecto): ").strip() or "reporte_resumen_general.txt"
            exportar_resumen_general_txt(ruta_archivo)
        elif opcion == '3':
            break
        else:
            print("Favor ingresar una de las opciones válidas\n")

# -----------------------------------------
# Menú principal
# Dirige a los submódulos del sistema tras la autenticación.
# Mantiene un bucle hasta que el usuario decide salir.
# -----------------------------------------
def menu_principal(nombre_usuario): # Menú principal después de iniciar sesión
    print(f"\nBienvenido Usuario {nombre_usuario}.")
    while True:
        print("\n--- Sistema de Gestión de Veterinaria ---")
        print("1.- Veterinarios")
        print("2.- Mascotas")
        print("3.- Reservas")
        print("4.- Reportes")
        print("5.- Salir\n")
         # Sistema de primer nivel de menú
        opcion = input("Favor ingresar opción: ").strip().lower() # input de la opción del menú
        print("")

        if opcion == '1':
            menu_veterinarios()
        elif opcion == '2':
            menu_mascotas()
        elif opcion == '3':
            menu_reservas()
        elif opcion == '4':
            menu_reportes()
        elif opcion == '5':
            print("Que tenga buen día <3.")
            break
        else:
            print("Favor ingresar una de las opciones válidas\n") # Mensaje de error para opción inválida

# -----------------------------------------
# Menú de Login y Registro
# - 'Ingresar' valida credenciales y abre el menú principal.
# - 'Registrar' crea un usuario nuevo si los campos no están vacíos.
# Las funciones de verificación/registro delegan seguridad a sg_funciones/controladores.
# -----------------------------------------
def menu_login(): # Menú de login y registro
    while True: # Bucle infinito para el menú de login
        print("\n--- Inicio de Sesión Sistema de Gestión de Veterinaria ---")
        print("1.- Ingresar")
        print("2.- Registrar")
        print("3.- Salir\n")

        opcion = input("Favor ingresar opción: ").lower().strip() # input de la opción del menú
        print("")

        if opcion == '1': # Opción de ingresar
            username = input("Favor ingresar usuario: ").strip()
            password = input("Favor ingresar contraseña: ").strip()
            if username == '' or password == '':
                print("\nFavor ingresar valor distinto a vacío.")
            else:
                # verificar_login devuelve True/False según credenciales válidas
                login = verificar_login(username, password)
                if login:
                    menu_principal(username)
                else:
                    print("\nUsuario o password incorrecto.")
        elif opcion == '2': # Opción de registrar
            username = input("Favor ingresar usuario: ").strip()
            email = input("Favor ingresar email: ").strip()
            password = input("Favor ingresar contraseña: ").strip()
            rol = input("Favor ingresar rol: ").strip()
            if username == '' or email == '' or password == '' or rol == '':
                print("\nFavor ingresar valor distinto a vacío.")
            else:
                # registrar_login se encarga de aplicar hashing/validaciones en capa inferior
                registrar_login(username, email, password, rol)
        elif opcion == '3':
            print("Que tenga buen día <3.") # Mensaje del equipo
            break # Salir del programa
        else:
            print("Favor ingresar una de las opciones válidas\n")

# ---------------------------------------------------------------------------------
# Punto de entrada del programa
# Inicia la aplicación mostrando el menú de login.
# Este bloque permite que el archivo sea importable sin ejecutar la UI.
# ---------------------------------------------------------------------------------
if __name__ == "__main__": # Punto de entrada del programa
    menu_login() # Llamar al menú de login
