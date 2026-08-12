from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from schemas.detalle_venta_schema import DetalleVentaRespuesta


class VentaCrear(BaseModel):
    id_usuario: int


class VentaConBoletoCrear(BaseModel):
    id_usuario: int
    id_funcion: int
    asiento: str
    codigo_boleto: str


class VentaActualizar(BaseModel):
    id_usuario: Optional[int] = None
    fecha_compra: Optional[datetime] = None


class VentaRespuesta(BaseModel):
    id: int
    id_usuario: int
    fecha_compra: datetime
    total: float


class VentaConBoletoRespuesta(BaseModel):
    venta: VentaRespuesta
    detalle: DetalleVentaRespuesta
