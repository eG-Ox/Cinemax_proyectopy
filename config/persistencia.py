import json
import os

from modelos.usuario import Usuario


_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARCHIVO_USUARIOS = os.path.join(_BASE, "datos_usuarios.json")


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


def cargar_usuarios(udao):
    datos = _cargar(ARCHIVO_USUARIOS)
    for item in datos:
        usuario = Usuario.from_dict(item)
        udao._UsuarioDAO__bd.append(usuario)
        if usuario.id >= udao._UsuarioDAO__cid:
            udao._UsuarioDAO__cid = usuario.id + 1
