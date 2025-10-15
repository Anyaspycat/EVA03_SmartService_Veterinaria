# main.py
# Trabajo Práctico N°3 - Programación Segura
# Integrantes:
# - ++
# - ++
# - ++

# Descripción: Programa principal que maneja el flujo de la aplicación de gestión de veterinaria.
# Permite a los usuarios registrarse, iniciar sesión y acceder a un menú principal con opciones para gestionar veterinarios, mascotas y reservas
# utilizando funciones definidas en otros módulos.
import sqlite3
from sg_veterinaria import *
from sg_funciones import *
# Crear las tablas necesarias al iniciar el programa
crear_tabla_usuarios() # Crear tabla usuarios si no existe
crear_tablas_veterinaria() # Crear tabla veterinarios si no existe
crear_tabla_mascotas() # Crear tabla mascotas si no existe
crear_tabla_reservas() # Crear tabla reservas si no existe

def menu_principal(username): # Menú principal después de iniciar sesión
    print(f"\nBienvenido Usuario {username}.")
    while True:
        print("\n--- Sistema de Gestión de Veterinaria ---")
        print("1.- Agregar Veterinarios")
        print("2.- Agregar Mascotas")
        print("3.- Agendar Reserva")
        print("4.- Listar Reservas")
        print("5.- Actualizar Reserva")
        print("6.- Eliminar Reserva")
        print("7.- Generar Reporte")
        print("8.- Salir\n")
        # Sistema de primer nivel de menú
        opc2 = input("Favor ingresar opcion: ").lower().strip() # input de la opción del menú
        print("")

        if opc2 == '1':
            continue
        elif opc2 == '2':
            continue
        elif opc2 == '3':
            continue
        elif opc2 == '4':
            continue
        elif opc2 == '5':
            continue
        elif opc2 == '6':
            continue
        elif opc2 == '7':
            continue
        elif opc2 == '8':
            print("Que tenga buen día <3.")
            break
        else:
            print("Favor ingresar una de las opciones válidas") # Mensaje de error para opción inválida

def menu_login(): # Menú de login y registro
    while True: # Bucle infinito para el menú de login
        print("\n--- Inicio de Sesión Sistema de Gestión de Veterinaria ---")
        print("1.- Ingresar")
        print("2.- Registrar")
        print("3.- Salir\n")

        opc = input("Favor ingresar opcion: ").lower().strip()
        print("") # input de la opción del menú

        if opc == '1': # Opción de ingresar
            username = input("Favor ingresar usuario: ").strip()
            password = input("Favor ingresar contraseña: ").strip()
            if username == '' or password == '':
                print("\nFavor ingresar valor distinto a vacío.")
            else:
                login = verificar_login(username, password)
                if login:
                    menu_principal(username)
                else:
                    print("\nUsuario o password incorrecto.")
        elif opc == '2': # Opción de registrar
            username = input("Favor ingresar usuario: ").strip()
            email = input("Favor ingresar email: ").strip()
            password = input("Favor ingresar contraseña: ").strip()
            rol = input("Favor ingresar rol: ").strip()
            if username == '' or email == '' or password == '' or rol == '':
                print("\nFavor ingresar valor distinto a vacío.")
            else:
                registrar_login(username, email, password, rol)
        elif opc == '3':
            print("Que tenga buen día <3.") # Mensaje del equipo
            break # Salir del programa
        else:
            print("Favor ingresar una de las opciones válidas\n")

if __name__ == "__main__": # Punto de entrada del programa
    menu_login() # Llamar al menú de login
