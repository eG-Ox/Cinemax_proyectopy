from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class VentaCrear(BaseModel):
    id_usuario: int
    fecha_compra: Optional[datetime] = None


class VentaActualizar(BaseModel):
    id_usuario: Optional[int] = None
    fecha_compra: Optional[datetime] = None


class VentaRespuesta(BaseModel):
    id: int
    id_usuario: int
    fecha_compra: datetime
