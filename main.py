from config.logger import Logger
from config.persistencia import cargar_usuarios, guardar_usuarios
from config.sistema_config import SistemaConfig
from dao.usuario_dao import UsuarioDAO
from vistas.menu import (
    actualizar_usuario,
    agregar_usuario,
    eliminar_usuario,
    listar_usuarios,
    mostrar_menu,
    ver_usuarios_json,
)


def main():
    cfg = SistemaConfig()
    udao = UsuarioDAO()

    Logger().info(f"Aplicacion cinemax abierta: {cfg.nombre} v{cfg.version}")
    cargar_usuarios(udao)

    while True:
        mostrar_menu(cfg)
        opcion = input(" Elige una opcion: ").strip()
        match opcion:
            case "1":
                agregar_usuario(udao)
            case "2":
                listar_usuarios(udao)
            case "3":
                actualizar_usuario(udao)
            case "4":
                eliminar_usuario(udao)
            case "5":
                ver_usuarios_json(udao)
            case "0":
                guardar_usuarios(udao)
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opcion no valida, elige entre 0 y 5")


if __name__ == "__main__":
    main()
