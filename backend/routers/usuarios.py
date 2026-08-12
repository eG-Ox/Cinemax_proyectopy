from fastapi import APIRouter, HTTPException
from dao.usuario_dao import (
    CorreoDuplicadoError,
    UsuarioConVentasError,
    UsuarioDAO,
    UsuarioNoEncontradoError,
)
from modelos.usuario import Usuario
from schemas.usuario_schema import UsuarioActualizar, UsuarioCrear, UsuarioRespuesta

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
dao = UsuarioDAO()


@router.get("/", response_model=list[UsuarioRespuesta])
def listar_usuarios():
    return [usuario.to_dict() for usuario in dao.obtener_todos()]


@router.get("/{usuario_id}", response_model=UsuarioRespuesta)
def obtener_usuario(usuario_id: int):
    usuario = dao.buscar_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario ID={usuario_id} no encontrado")
    return usuario.to_dict()


@router.post("/", response_model=UsuarioRespuesta, status_code=201)
def crear_usuario(datos: UsuarioCrear):
    try:
        usuario = dao.insertar(Usuario(datos.nombres_usuario, datos.correo))
        return usuario.to_dict()
    except CorreoDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.put("/{usuario_id}", response_model=UsuarioRespuesta)
def actualizar_usuario(usuario_id: int, datos: UsuarioActualizar):
    try:
        usuario = dao.actualizar(usuario_id, datos.nombres_usuario, datos.correo)
        return usuario.to_dict()
    except UsuarioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CorreoDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    try:
        dao.eliminar(usuario_id)
        return {"mensaje": f"Usuario ID={usuario_id} eliminado"}
    except UsuarioNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except UsuarioConVentasError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
