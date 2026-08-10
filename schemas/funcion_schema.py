from datetime import date, time
from pydantic import BaseModel, field_validator
from typing import Optional


class FuncionCrear(BaseModel):
    id_pelicula: int
    id_sala: int
    fecha_funcion: date
    hora: time
    precio: float

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        return valor


class FuncionActualizar(BaseModel):
    id_pelicula: Optional[int] = None
    id_sala: Optional[int] = None
    fecha_funcion: Optional[date] = None
    hora: Optional[time] = None
    precio: Optional[float] = None

    @field_validator("precio")
    @classmethod
    def validar_precio(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        return valor


class FuncionRespuesta(BaseModel):
    id: int
    id_pelicula: int
    id_sala: int
    fecha_funcion: date
    hora: time
    precio: float
