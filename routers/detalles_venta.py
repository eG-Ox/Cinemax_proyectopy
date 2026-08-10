from fastapi import APIRouter, HTTPException
from dao.detalle_venta_dao import (
    CodigoBoletoDuplicadoError,
    DetalleVentaDAO,
    DetalleVentaNoEncontradoError,
    ReferenciaDetalleInvalidaError,
)
from dao.funcion_dao import FuncionDAO
from dao.venta_dao import VentaDAO
from modelos.detalle_venta import DetalleVenta
from schemas.detalle_venta_schema import (
    DetalleVentaActualizar,
    DetalleVentaCrear,
    DetalleVentaRespuesta,
)

router = APIRouter(prefix="/detalles-venta", tags=["Detalles de venta"])
dao = DetalleVentaDAO()
vdao = VentaDAO()
fdao = FuncionDAO()


@router.get("/", response_model=list[DetalleVentaRespuesta])
def listar_detalles():
    return [detalle.to_dict() for detalle in dao.obtener_todos()]


@router.get("/venta/{venta_id}", response_model=list[DetalleVentaRespuesta])
def detalles_por_venta(venta_id: int):
    if not vdao.buscar_por_id(venta_id):
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    return [detalle.to_dict() for detalle in dao.buscar_por_venta(venta_id)]


@router.get("/{detalle_id}", response_model=DetalleVentaRespuesta)
def obtener_detalle(detalle_id: int):
    detalle = dao.buscar_por_id(detalle_id)
    if not detalle:
        raise HTTPException(status_code=404, detail=f"Detalle de venta ID={detalle_id} no encontrado")
    return detalle.to_dict()


@router.post("/", response_model=DetalleVentaRespuesta, status_code=201)
def crear_detalle(datos: DetalleVentaCrear):
    try:
        detalle = dao.insertar(
            DetalleVenta(
                datos.id_venta,
                datos.id_funcion,
                datos.asiento,
                datos.codigo_boleto,
            ),
            vdao,
            fdao,
        )
        return detalle.to_dict()
    except ReferenciaDetalleInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CodigoBoletoDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.put("/{detalle_id}", response_model=DetalleVentaRespuesta)
def actualizar_detalle(detalle_id: int, datos: DetalleVentaActualizar):
    try:
        detalle = dao.actualizar(
            detalle_id,
            datos.id_venta,
            datos.id_funcion,
            datos.asiento,
            datos.codigo_boleto,
            vdao,
            fdao,
        )
        return detalle.to_dict()
    except DetalleVentaNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except ReferenciaDetalleInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CodigoBoletoDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.delete("/{detalle_id}")
def eliminar_detalle(detalle_id: int):
    try:
        dao.eliminar(detalle_id)
        return {"mensaje": f"Detalle de venta ID={detalle_id} eliminado"}
    except DetalleVentaNoEncontradoError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
