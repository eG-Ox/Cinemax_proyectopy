from config.logger import Logger
from config.persistencia import cargar_todo, guardar_todo
from config.sistema_config import SistemaConfig
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import SalaDAO
from dao.usuario_dao import UsuarioDAO
from vistas.menu import (
    actualizar_pelicula,
    actualizar_sala,
    actualizar_usuario,
    agregar_pelicula,
    agregar_sala,
    agregar_usuario,
    eliminar_pelicula,
    eliminar_sala,
    eliminar_usuario,
    listar_peliculas,
    listar_salas,
    listar_usuarios,
    mostrar_menu,
    ver_peliculas_json,
    ver_salas_json,
    ver_usuarios_json,
)


def main():
    cfg = SistemaConfig()
    udao = UsuarioDAO()
    pdao = PeliculaDAO()
    sdao = SalaDAO()

    Logger().info(f"Aplicacion cinemax abierta: {cfg.nombre} v{cfg.version}")
    cargar_todo(udao, pdao, sdao)

    while True:
        mostrar_menu(cfg)
        opcion = input(" Elige una opcion: ").strip()
        match opcion:
            case "1":
                agregar_usuario(udao)
            case "2":
                agregar_pelicula(pdao)
            case "3":
                agregar_sala(sdao)
            case "4":
                listar_usuarios(udao)
            case "5":
                listar_peliculas(pdao)
            case "6":
                listar_salas(sdao)
            case "7":
                actualizar_usuario(udao)
            case "8":
                actualizar_pelicula(pdao)
            case "9":
                actualizar_sala(sdao)
            case "10":
                eliminar_usuario(udao)
            case "11":
                eliminar_pelicula(pdao)
            case "12":
                eliminar_sala(sdao)
            case "13":
                ver_usuarios_json(udao)
            case "14":
                ver_peliculas_json(pdao)
            case "15":
                ver_salas_json(sdao)
            case "16":
                guardar_todo(udao, pdao, sdao)
                print(" OK Datos guardados en JSON")
            case "17":
                Logger().mostrar_logs()
            case "18":
                Logger().limpiar()
                print(" OK Historial de logs limpiado")
            case "0":
                guardar_todo(udao, pdao, sdao)
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opcion no valida, elige entre 0 y 18")


if __name__ == "__main__":
    main()
