from config.logger import Logger
from config.sistema_config import SistemaConfig
from dao.usuario_dao import UsuarioDAO
from vistas.menu import mostrar_menu, agregar_usuario, listar_usuarios


def main():
    cfg = SistemaConfig()
    udao = UsuarioDAO()

    Logger().info(f"Aplicacion cinemax abierta: {cfg.nombre} v{cfg.version}")

    while True:
        mostrar_menu(cfg)
        opcion = input(" Elige una opción: ").strip()
        match opcion:
            case "1":
                agregar_usuario(udao)
            case "2":
                listar_usuarios(udao)
            case "0":
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opción no válida")


if __name__ == "__main__":
    main()
