import json
import os

from modelos.funcion import Funcion
from modelos.pelicula import Pelicula
from modelos.sala import Sala
from modelos.usuario import Usuario


_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_USUARIOS = os.path.join(_BASE, "datos_usuarios.json")
ARCHIVO_PELICULAS = os.path.join(_BASE, "datos_peliculas.json")
ARCHIVO_SALAS = os.path.join(_BASE, "datos_salas.json")
ARCHIVO_FUNCIONES = os.path.join(_BASE, "datos_funciones.json")


def _guardar(archivo, objetos):
    datos = [objeto.to_dict() for objeto in objetos]
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def _cargar(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def guardar_usuarios(udao):
    _guardar(ARCHIVO_USUARIOS, udao.obtener_todos())


def guardar_peliculas(pdao):
    _guardar(ARCHIVO_PELICULAS, pdao.obtener_todos())


def guardar_salas(sdao):
    _guardar(ARCHIVO_SALAS, sdao.obtener_todos())


def guardar_funciones(fdao):
    _guardar(ARCHIVO_FUNCIONES, fdao.obtener_todos())


def cargar_usuarios(udao):
    datos = _cargar(ARCHIVO_USUARIOS)
    for item in datos:
        usuario = Usuario.from_dict(item)
        udao._UsuarioDAO__bd.append(usuario)
        if usuario.id >= udao._UsuarioDAO__cid:
            udao._UsuarioDAO__cid = usuario.id + 1


def cargar_peliculas(pdao):
    datos = _cargar(ARCHIVO_PELICULAS)
    for item in datos:
        pelicula = Pelicula.from_dict(item)
        pdao._PeliculaDAO__bd.append(pelicula)
        if pelicula.id >= pdao._PeliculaDAO__cid:
            pdao._PeliculaDAO__cid = pelicula.id + 1


def cargar_salas(sdao):
    datos = _cargar(ARCHIVO_SALAS)
    for item in datos:
        sala = Sala.from_dict(item)
        sdao._SalaDAO__bd.append(sala)
        if sala.id >= sdao._SalaDAO__cid:
            sdao._SalaDAO__cid = sala.id + 1


def cargar_funciones(fdao):
    datos = _cargar(ARCHIVO_FUNCIONES)
    for item in datos:
        funcion = Funcion.from_dict(item)
        fdao._FuncionDAO__bd.append(funcion)
        if funcion.id >= fdao._FuncionDAO__cid:
            fdao._FuncionDAO__cid = funcion.id + 1


def guardar_todo(udao, pdao, sdao, fdao=None):
    guardar_usuarios(udao)
    guardar_peliculas(pdao)
    guardar_salas(sdao)
    if fdao is not None:
        guardar_funciones(fdao)


def cargar_todo(udao, pdao, sdao, fdao=None):
    cargar_usuarios(udao)
    cargar_peliculas(pdao)
    cargar_salas(sdao)
    if fdao is not None:
        cargar_funciones(fdao)
