import sqlite3
from sg_veterinaria import *
from sg_funciones import *

crear_tabla_usuarios()
crear_tablas_veterinaria()
crear_tabla_mascotas()
crear_tabla_reservas()

def menu_principal(username):
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

        opc2 = input("Favor ingresar opcion: ").lower().strip()
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
            print("Favor ingresar una de las opciones válidas")

def menu_login():
    while True:
        print("\n--- Inicio de Sesión Sistema de Gestión de Veterinaria ---")
        print("1.- Ingresar")
        print("2.- Registrar")
        print("3.- Salir\n")

        opc = input("Favor ingresar opcion: ").lower().strip()
        print("")

        if opc == '1':
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
        elif opc == '2':
            username = input("Favor ingresar usuario: ").strip()
            email = input("Favor ingresar email: ").strip()
            password = input("Favor ingresar contraseña: ").strip()
            rol = input("Favor ingresar rol: ").strip()
            if username == '' or email == '' or password == '' or rol == '':
                print("\nFavor ingresar valor distinto a vacío.")
            else:
                registrar_login(username, email, password, rol)
        elif opc == '3':
            print("Que tenga buen día <3.")
            break
        else:
            print("Favor ingresar una de las opciones válidas\n")

if __name__ == "__main__":
    menu_login()
