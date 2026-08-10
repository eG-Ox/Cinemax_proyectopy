from fastapi import APIRouter, HTTPException
from dao.funcion_dao import (
    FuncionConDetallesError,
    FuncionDAO,
    FuncionNoEncontradaError,
    ReferenciaInvalidaError,
)
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import SalaDAO
from modelos.funcion import Funcion
from schemas.funcion_schema import FuncionActualizar, FuncionCrear, FuncionRespuesta

router = APIRouter(prefix="/funciones", tags=["Funciones"])
dao = FuncionDAO()
pdao = PeliculaDAO()
sdao = SalaDAO()


@router.get("/", response_model=list[FuncionRespuesta])
def listar_funciones():
    return [funcion.to_dict() for funcion in dao.obtener_todos()]


@router.get("/{funcion_id}", response_model=FuncionRespuesta)
def obtener_funcion(funcion_id: int):
    funcion = dao.buscar_por_id(funcion_id)
    if not funcion:
        raise HTTPException(status_code=404, detail=f"Funcion ID={funcion_id} no encontrada")
    return funcion.to_dict()


@router.post("/", response_model=FuncionRespuesta, status_code=201)
def crear_funcion(datos: FuncionCrear):
    try:
        funcion = dao.insertar(
            Funcion(
                datos.id_pelicula,
                datos.id_sala,
                datos.fecha_funcion,
                datos.hora,
                datos.precio,
            ),
            pdao,
            sdao,
        )
        return funcion.to_dict()
    except ReferenciaInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.put("/{funcion_id}", response_model=FuncionRespuesta)
def actualizar_funcion(funcion_id: int, datos: FuncionActualizar):
    try:
        funcion = dao.actualizar(
            funcion_id,
            datos.id_pelicula,
            datos.id_sala,
            datos.fecha_funcion,
            datos.hora,
            datos.precio,
            pdao,
            sdao,
        )
        return funcion.to_dict()
    except FuncionNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except ReferenciaInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/{funcion_id}")
def eliminar_funcion(funcion_id: int):
    try:
        dao.eliminar(funcion_id)
        return {"mensaje": f"Funcion ID={funcion_id} eliminada"}
    except FuncionNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except FuncionConDetallesError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
