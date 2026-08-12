from fastapi import APIRouter, HTTPException
from dao.pelicula_dao import (
    PeliculaConFuncionesError,
    PeliculaDAO,
    PeliculaNoEncontradaError,
)
from modelos.pelicula import Pelicula
from schemas.pelicula_schema import PeliculaActualizar, PeliculaCrear, PeliculaRespuesta

router = APIRouter(prefix="/peliculas", tags=["Peliculas"])
dao = PeliculaDAO()


@router.get("/", response_model=list[PeliculaRespuesta])
def listar_peliculas():
    return [pelicula.to_dict() for pelicula in dao.obtener_todos()]


@router.get("/{pelicula_id}", response_model=PeliculaRespuesta)
def obtener_pelicula(pelicula_id: int):
    pelicula = dao.buscar_por_id(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail=f"Pelicula ID={pelicula_id} no encontrada")
    return pelicula.to_dict()


@router.post("/", response_model=PeliculaRespuesta, status_code=201)
def crear_pelicula(datos: PeliculaCrear):
    pelicula = dao.insertar(
        Pelicula(datos.titulo, datos.genero, datos.clasificacion, datos.duracion)
    )
    return pelicula.to_dict()


@router.put("/{pelicula_id}", response_model=PeliculaRespuesta)
def actualizar_pelicula(pelicula_id: int, datos: PeliculaActualizar):
    try:
        pelicula = dao.actualizar(
            pelicula_id,
            datos.titulo,
            datos.genero,
            datos.clasificacion,
            datos.duracion,
        )
        return pelicula.to_dict()
    except PeliculaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int):
    try:
        dao.eliminar(pelicula_id)
        return {"mensaje": f"Pelicula ID={pelicula_id} eliminada"}
    except PeliculaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except PeliculaConFuncionesError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
