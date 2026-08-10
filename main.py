from config.logger import Logger
from config.persistencia import cargar_todo, guardar_todo
from config.sistema_config import SistemaConfig
from dao.detalle_venta_dao import DetalleVentaDAO
from dao.funcion_dao import FuncionDAO
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import SalaDAO
from dao.usuario_dao import UsuarioDAO
from dao.venta_dao import VentaDAO
from vistas.menu import mostrar_menu,agregar_usuario,agregar_pelicula,agregar_sala,agregar_funcion,agregar_venta,agregar_detalle_venta,listar_usuarios,listar_peliculas,listar_salas,listar_funciones,listar_ventas,listar_detalles_venta,eliminar_usuario,eliminar_pelicula,eliminar_sala,eliminar_funcion,eliminar_venta,eliminar_detalle_venta,actualizar_usuario,actualizar_pelicula,actualizar_sala,actualizar_funcion,actualizar_venta,actualizar_detalle_venta,ver_usuarios_json,ver_peliculas_json,ver_salas_json,ver_funciones_json,ver_ventas_json,ver_detalles_json


def main():
    cfg = SistemaConfig()
    udao = UsuarioDAO()
    pdao = PeliculaDAO()
    sdao = SalaDAO()
    fdao = FuncionDAO()
    vdao = VentaDAO()
    ddao = DetalleVentaDAO()

    cargar_todo(udao, pdao, sdao, fdao, vdao, ddao)

    while True:
        mostrar_menu(cfg)
        opcion = input(" Elige una opción: ").strip()
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
                agregar_venta(vdao, udao)
            case "6":
                agregar_detalle_venta(ddao, vdao, fdao)
            case "7":
                listar_usuarios(udao)
            case "8":
                listar_peliculas(pdao)
            case "9":
                listar_salas(sdao)
            case "10":
                listar_funciones(fdao)
            case "11":
                listar_ventas(vdao)
            case "12":
                listar_detalles_venta(ddao)
            case "13":
                eliminar_usuario(udao)
            case "14":
                eliminar_pelicula(pdao)
            case "15":
                eliminar_sala(sdao)
            case "16":
                eliminar_funcion(fdao)
            case "17":
                eliminar_venta(vdao)
            case "18":
                eliminar_detalle_venta(ddao)
            case "19":
                actualizar_usuario(udao)
            case "20":
                actualizar_pelicula(pdao)
            case "21":
                actualizar_sala(sdao)
            case "22":
                actualizar_funcion(fdao, pdao, sdao)
            case "23":
                actualizar_venta(vdao, udao)
            case "24":
                actualizar_detalle_venta(ddao, vdao, fdao)
            case "25":
                ver_usuarios_json(udao)
            case "26":
                ver_peliculas_json(pdao)
            case "27":
                ver_salas_json(sdao)
            case "28":
                ver_funciones_json(fdao)
            case "29":
                ver_ventas_json(vdao)
            case "30":
                ver_detalles_json(ddao)
            case "31":
                guardar_todo(udao, pdao, sdao, fdao, vdao, ddao)
            case "32":
                Logger().mostrar_logs()
            case "33":
                Logger().limpiar()
            case "0":
                guardar_todo(udao, pdao, sdao, fdao, vdao, ddao)
                Logger().info("Sistema cerrado por el usuario")
                print("\n Hasta luego.")
                break
            case _:
                print(" Opción no válida, elige entre 0 y 33")


if __name__ == "__main__":
    main()
