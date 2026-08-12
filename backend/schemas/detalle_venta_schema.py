from pydantic import BaseModel
from typing import Optional


class DetalleVentaCrear(BaseModel):
    id_venta: int
    id_funcion: int
    asiento: str
    codigo_boleto: str


class DetalleVentaActualizar(BaseModel):
    id_venta: Optional[int] = None
    id_funcion: Optional[int] = None
    asiento: Optional[str] = None
    codigo_boleto: Optional[str] = None


class DetalleVentaRespuesta(BaseModel):
    id: int
    id_venta: int
    id_funcion: int
    asiento: str
    codigo_boleto: str
