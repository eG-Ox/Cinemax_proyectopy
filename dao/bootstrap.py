from dao.detalle_venta_dao import DetalleVentaDAO
from dao.funcion_dao import FuncionDAO
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import SalaDAO
from dao.usuario_dao import UsuarioDAO
from dao.venta_dao import VentaDAO


def crear_daos():
    return {
        "usuarios": UsuarioDAO(),
        "peliculas": PeliculaDAO(),
        "salas": SalaDAO(),
        "funciones": FuncionDAO(),
        "ventas": VentaDAO(),
        "detalles": DetalleVentaDAO(),
    }
