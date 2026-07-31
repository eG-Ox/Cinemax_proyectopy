from config.logger import Logger
from config.persistencia import cargar_todo, guardar_todo
from config.sistema_config import SistemaConfig
from dao.funcion_dao import FuncionDAO
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import SalaDAO
from dao.usuario_dao import UsuarioDAO
from vistas.menu import (
    actualizar_funcion,
    actualizar_pelicula,
    actualizar_sala,
    actualizar_usuario,
    agregar_funcion,
    agregar_pelicula,
    agregar_sala,
    agregar_usuario,
    eliminar_funcion,
    eliminar_pelicula,
    eliminar_sala,
    eliminar_usuario,
    listar_funciones,
    listar_peliculas,
    listar_salas,
    listar_usuarios,
    mostrar_menu,
    ver_funciones_json,
    ver_peliculas_json,
    ver_salas_json,
    ver_usuarios_json,
)


def main():
    cfg = SistemaConfig()
    udao = UsuarioDAO()
    pdao = PeliculaDAO()
    sdao = SalaDAO()
    fdao = FuncionDAO()

    Logger().info(f"Aplicacion cinemax abierta: {cfg.nombre} v{cfg.version}")
    cargar_todo(udao, pdao, sdao, fdao)

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
                agregar_funcion(fdao, pdao, sdao)
            case "5":
                listar_usuarios(udao)
            case "6":
                listar_peliculas(pdao)
            case "7":
                listar_salas(sdao)
            case "8":
                listar_funciones(fdao)
            case "9":
                actualizar_usuario(udao)
            case "10":
                actualizar_pelicula(pdao)
            case "11":
                actualizar_sala(sdao)
            case "12":
                actualizar_funcion(fdao, pdao, sdao)
            case "13":
                eliminar_usuario(udao)
            case "14":
                eliminar_pelicula(pdao)
            case "15":
                eliminar_sala(sdao)
            case "16":
                eliminar_funcion(fdao)
            case "17":
                ver_usuarios_json(udao)
            case "18":
                ver_peliculas_json(pdao)
            case "19":
                ver_salas_json(sdao)
            case "20":
                ver_funciones_json(fdao)
            case "21":
                guardar_todo(udao, pdao, sdao, fdao)
                print(" OK Datos guardados en JSON")
            case "22":
                Logger().mostrar_logs()
            case "23":
                Logger().limpiar()
                print(" OK Historial de logs limpiado")
            case "0":
                guardar_todo(udao, pdao, sdao, fdao)
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opcion no valida, elige entre 0 y 23")


if __name__ == "__main__":
    main()
