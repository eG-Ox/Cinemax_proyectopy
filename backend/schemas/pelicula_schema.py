from pydantic import BaseModel, field_validator
from typing import Optional


class PeliculaCrear(BaseModel):
    titulo: str
    genero: str
    clasificacion: str
    duracion: int

    @field_validator("duracion")
    @classmethod
    def validar_duracion(cls, valor):
        if valor <= 0:
            raise ValueError("La duracion debe ser mayor que cero")
        return valor


class PeliculaActualizar(BaseModel):
    titulo: Optional[str] = None
    genero: Optional[str] = None
    clasificacion: Optional[str] = None
    duracion: Optional[int] = None

    @field_validator("duracion")
    @classmethod
    def validar_duracion(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("La duracion debe ser mayor que cero")
        return valor


class PeliculaRespuesta(BaseModel):
    id: int
    titulo: str
    genero: str
    clasificacion: str
    duracion: int
