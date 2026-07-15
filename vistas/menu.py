def mostrar_menu(cfg):
    print(f"\n{'=' * 40}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 40}")
    print(" 1. Agregar usuario")
    print(" 2. Listar usuarios")
    print(" 0. Salir")
    print(f"{'=' * 40}")


def agregar_usuario(udao):
    print("\n--- AGREGAR USUARIO ---")
    nombres_usuario = input(" Nombres : ")
    correo = input(" Correo : ")
    usuario = udao.insertar(__import__("modelos.usuario", fromlist=["Usuario"]).Usuario(nombres_usuario, correo))
    print(f" OK Usuario agregado con ID={usuario.id}")


def listar_usuarios(udao):
    print("\n--- USUARIOS ---")
    usuarios = udao.obtener_todos()
    if usuarios:
        for usuario in usuarios:
            print(f" {usuario}")
    else:
        print(" (No hay usuarios registrados)")
