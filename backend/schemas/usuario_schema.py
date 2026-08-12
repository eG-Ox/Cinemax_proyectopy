from pydantic import BaseModel
from typing import Optional


class UsuarioCrear(BaseModel):
    nombres_usuario: str
    correo: str


class UsuarioActualizar(BaseModel):
    nombres_usuario: Optional[str] = None
    correo: Optional[str] = None


class UsuarioRespuesta(BaseModel):
    id: int
    nombres_usuario: str
    correo: str
