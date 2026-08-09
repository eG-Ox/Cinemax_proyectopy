import json
import os

from modelos.detalle_venta import DetalleVenta
from modelos.funcion import Funcion
from modelos.pelicula import Pelicula
from modelos.sala import Sala
from modelos.usuario import Usuario
from modelos.venta import Venta


_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_USUARIOS = os.path.join(_BASE, "datos_usuarios.json")
ARCHIVO_PELICULAS = os.path.join(_BASE, "datos_peliculas.json")
ARCHIVO_SALAS = os.path.join(_BASE, "datos_salas.json")
ARCHIVO_FUNCIONES = os.path.join(_BASE, "datos_funciones.json")
ARCHIVO_VENTAS = os.path.join(_BASE, "datos_ventas.json")
ARCHIVO_DETALLES = os.path.join(_BASE, "datos_detalles_venta.json")


def _guardar(archivo, objetos):
    datos = [objeto.to_dict() for objeto in objetos]
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
    print(f" OK Datos guardados en '{archivo}'")


def _cargar(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f" AVISO: No existe '{archivo}', se empieza desde cero")
        return []


def guardar_usuarios(udao):
    _guardar(ARCHIVO_USUARIOS, udao.obtener_todos())


def guardar_peliculas(pdao):
    _guardar(ARCHIVO_PELICULAS, pdao.obtener_todos())


def guardar_salas(sdao):
    _guardar(ARCHIVO_SALAS, sdao.obtener_todos())


def guardar_funciones(fdao):
    _guardar(ARCHIVO_FUNCIONES, fdao.obtener_todos())


def guardar_ventas(vdao):
    _guardar(ARCHIVO_VENTAS, vdao.obtener_todos())


def guardar_detalles(ddao):
    _guardar(ARCHIVO_DETALLES, ddao.obtener_todos())


def cargar_usuarios(udao):
    datos = _cargar(ARCHIVO_USUARIOS)
    for d in datos:
        usuario = Usuario.from_dict(d)
        udao._UsuarioDAO__bd.append(usuario)
        if usuario.id >= udao._UsuarioDAO__cid:
            udao._UsuarioDAO__cid = usuario.id + 1
    if datos:
        print(f" OK {len(datos)} usuarios cargados desde '{ARCHIVO_USUARIOS}'")


def cargar_peliculas(pdao):
    datos = _cargar(ARCHIVO_PELICULAS)
    for d in datos:
        pelicula = Pelicula.from_dict(d)
        pdao._PeliculaDAO__bd.append(pelicula)
        if pelicula.id >= pdao._PeliculaDAO__cid:
            pdao._PeliculaDAO__cid = pelicula.id + 1
    if datos:
        print(f" OK {len(datos)} peliculas cargadas desde '{ARCHIVO_PELICULAS}'")


def cargar_salas(sdao):
    datos = _cargar(ARCHIVO_SALAS)
    for d in datos:
        sala = Sala.from_dict(d)
        sdao._SalaDAO__bd.append(sala)
        if sala.id >= sdao._SalaDAO__cid:
            sdao._SalaDAO__cid = sala.id + 1
    if datos:
        print(f" OK {len(datos)} salas cargadas desde '{ARCHIVO_SALAS}'")


def cargar_funciones(fdao):
    datos = _cargar(ARCHIVO_FUNCIONES)
    for d in datos:
        funcion = Funcion.from_dict(d)
        fdao._FuncionDAO__bd.append(funcion)
        if funcion.id >= fdao._FuncionDAO__cid:
            fdao._FuncionDAO__cid = funcion.id + 1
    if datos:
        print(f" OK {len(datos)} funciones cargadas desde '{ARCHIVO_FUNCIONES}'")


def cargar_ventas(vdao):
    datos = _cargar(ARCHIVO_VENTAS)
    for d in datos:
        venta = Venta.from_dict(d)
        vdao._VentaDAO__bd.append(venta)
        if venta.id >= vdao._VentaDAO__cid:
            vdao._VentaDAO__cid = venta.id + 1
    if datos:
        print(f" OK {len(datos)} ventas cargadas desde '{ARCHIVO_VENTAS}'")


def cargar_detalles(ddao):
    datos = _cargar(ARCHIVO_DETALLES)
    for d in datos:
        detalle = DetalleVenta.from_dict(d)
        ddao._DetalleVentaDAO__bd.append(detalle)
        if detalle.id >= ddao._DetalleVentaDAO__cid:
            ddao._DetalleVentaDAO__cid = detalle.id + 1
    if datos:
        print(f" OK {len(datos)} detalles cargados desde '{ARCHIVO_DETALLES}'")


def guardar_todo(udao, pdao, sdao, fdao, vdao, ddao):
    guardar_usuarios(udao)
    guardar_peliculas(pdao)
    guardar_salas(sdao)
    guardar_funciones(fdao)
    guardar_ventas(vdao)
    guardar_detalles(ddao)


def cargar_todo(udao, pdao, sdao, fdao, vdao, ddao):
    cargar_usuarios(udao)
    cargar_peliculas(pdao)
    cargar_salas(sdao)
    cargar_funciones(fdao)
    cargar_ventas(vdao)
    cargar_detalles(ddao)
