import json

from dao.usuario_dao import CorreoDuplicadoError, UsuarioNoEncontradoError
from modelos.usuario import Usuario


def mostrar_menu(cfg):
    print(f"\n{'=' * 40}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 40}")
    print(" 1. Agregar usuario")
    print(" 2. Listar usuarios")
    print(" 3. Actualizar usuario")
    print(" 4. Eliminar usuario")
    print(" 5. Ver usuarios en JSON")
    print(" 0. Salir")
    print(f"{'=' * 40}")


def agregar_usuario(udao):
    print("\n--- AGREGAR USUARIO ---")
    nombres_usuario = input(" Nombres : ")
    correo = input(" Correo : ")
    try:
        usuario = udao.insertar(Usuario(nombres_usuario, correo))
        print(f" OK Usuario agregado con ID={usuario.id}")
    except CorreoDuplicadoError as ex:
        print(f" ERROR: {ex}")


def listar_usuarios(udao):
    print("\n--- USUARIOS ---")
    usuarios = udao.obtener_todos()
    if usuarios:
        for usuario in usuarios:
            print(f" {usuario}")
    else:
        print(" (No hay usuarios registrados)")


def actualizar_usuario(udao):
    print("\n--- ACTUALIZAR USUARIO ---")
    try:
        usuario_id = int(input(" ID del usuario a actualizar: "))
        nombres_usuario = input(" Nuevos nombres (Enter para no cambiar): ").strip()
        correo = input(" Nuevo correo (Enter para no cambiar): ").strip()
        usuario = udao.actualizar(usuario_id, nombres_usuario or None, correo or None)
        print(f" OK Usuario actualizado: {usuario}")
    except (UsuarioNoEncontradoError, CorreoDuplicadoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_usuario(udao):
    print("\n--- ELIMINAR USUARIO ---")
    try:
        usuario_id = int(input(" ID del usuario a eliminar: "))
        udao.eliminar(usuario_id)
        print(f" OK Usuario ID={usuario_id} eliminado")
    except UsuarioNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def ver_usuarios_json(udao):
    print("\n--- USUARIOS EN JSON ---")
    usuarios = udao.obtener_todos()
    if usuarios:
        print(json.dumps([usuario.to_dict() for usuario in usuarios], indent=4, ensure_ascii=False))
    else:
        print(" (No hay usuarios registrados)")
