from fastapi import APIRouter, HTTPException
from dao.pelicula_dao import PeliculaDAO
from dao.sala_dao import (
    CapacidadSalaInsuficienteError,
    ReferenciaPeliculaSalaInvalidaError,
    SalaConFuncionesError,
    SalaDAO,
    SalaNoEncontradaError,
)
from modelos.sala import Sala
from schemas.sala_schema import SalaActualizar, SalaCrear, SalaRespuesta

router = APIRouter(prefix="/salas", tags=["Salas"])
dao = SalaDAO()
pdao = PeliculaDAO()


@router.get("/", response_model=list[SalaRespuesta])
def listar_salas():
    return [sala.to_dict() for sala in dao.obtener_todos()]


@router.get("/pelicula/{pelicula_id}", response_model=list[SalaRespuesta])
def salas_por_pelicula(pelicula_id: int):
    if not pdao.buscar_por_id(pelicula_id):
        raise HTTPException(status_code=404, detail=f"Pelicula ID={pelicula_id} no encontrada")
    return [sala.to_dict() for sala in dao.buscar_por_pelicula(pelicula_id)]


@router.get("/{sala_id}", response_model=SalaRespuesta)
def obtener_sala(sala_id: int):
    sala = dao.buscar_por_id(sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail=f"Sala ID={sala_id} no encontrada")
    return sala.to_dict()


@router.post("/", response_model=SalaRespuesta, status_code=201)
def crear_sala(datos: SalaCrear):
    try:
        sala = dao.insertar(Sala(datos.id_pelicula, datos.nombre_sala, datos.capacidad), pdao)
        return sala.to_dict()
    except ReferenciaPeliculaSalaInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.put("/{sala_id}", response_model=SalaRespuesta)
def actualizar_sala(sala_id: int, datos: SalaActualizar):
    try:
        sala = dao.actualizar(
            sala_id,
            datos.id_pelicula,
            datos.nombre_sala,
            datos.capacidad,
            pdao,
        )
        return sala.to_dict()
    except SalaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except ReferenciaPeliculaSalaInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CapacidadSalaInsuficienteError as ex:
        raise HTTPException(status_code=409, detail=str(ex))


@router.delete("/{sala_id}")
def eliminar_sala(sala_id: int):
    try:
        dao.eliminar(sala_id)
        return {"mensaje": f"Sala ID={sala_id} eliminada"}
    except SalaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except SalaConFuncionesError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
