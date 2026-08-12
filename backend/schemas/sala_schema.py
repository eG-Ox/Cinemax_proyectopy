from pydantic import BaseModel, field_validator
from typing import Optional


class SalaCrear(BaseModel):
    nombre_sala: str
    capacidad: int

    @field_validator("capacidad")
    @classmethod
    def validar_capacidad(cls, valor):
        if valor <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")
        return valor


class SalaActualizar(BaseModel):
    nombre_sala: Optional[str] = None
    capacidad: Optional[int] = None

    @field_validator("capacidad")
    @classmethod
    def validar_capacidad(cls, valor):
        if valor is not None and valor <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")
        return valor


class SalaRespuesta(BaseModel):
    id: int
    nombre_sala: str
    capacidad: int
