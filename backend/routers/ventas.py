from datetime import datetime
from fastapi import APIRouter, HTTPException
from dao.detalle_venta_dao import (
    AsientoOcupadoError,
    CodigoBoletoDuplicadoError,
    ReferenciaDetalleInvalidaError,
)
from dao.funcion_dao import FuncionDAO
from dao.usuario_dao import UsuarioDAO
from dao.venta_dao import (
    ReferenciaUsuarioInvalidaError,
    VentaConDetallesError,
    VentaDAO,
    VentaNoEncontradaError,
)
from modelos.detalle_venta import DetalleVenta
from modelos.venta import Venta
from schemas.venta_schema import (
    VentaActualizar,
    VentaConBoletoCrear,
    VentaConBoletoRespuesta,
    VentaCrear,
    VentaRespuesta,
)

router = APIRouter(prefix="/ventas", tags=["Ventas"])
dao = VentaDAO()
udao = UsuarioDAO()
fdao = FuncionDAO()


@router.get("/", response_model=list[VentaRespuesta])
def listar_ventas():
    return [venta.to_dict() for venta in dao.obtener_todos()]


@router.get("/usuario/{usuario_id}", response_model=list[VentaRespuesta])
def ventas_por_usuario(usuario_id: int):
    if not udao.buscar_por_id(usuario_id):
        raise HTTPException(status_code=404, detail=f"Usuario ID={usuario_id} no encontrado")
    return [venta.to_dict() for venta in dao.buscar_por_usuario(usuario_id)]


@router.get("/{venta_id}", response_model=VentaRespuesta)
def obtener_venta(venta_id: int):
    venta = dao.buscar_por_id(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail=f"Venta ID={venta_id} no encontrada")
    return venta.to_dict()


@router.post("/", response_model=VentaRespuesta, status_code=201)
def crear_venta(datos: VentaCrear):
    try:
        venta = dao.insertar(
            Venta(datos.id_usuario, datos.fecha_compra or datetime.now()),
            udao,
        )
        return venta.to_dict()
    except ReferenciaUsuarioInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.post("/con-boleto", response_model=VentaConBoletoRespuesta, status_code=201)
def crear_venta_con_boleto(datos: VentaConBoletoCrear):
    try:
        venta, detalle = dao.insertar_con_detalle(
            Venta(datos.id_usuario, datos.fecha_compra or datetime.now()),
            DetalleVenta(
                None,
                datos.id_funcion,
                datos.asiento,
                datos.codigo_boleto,
            ),
            udao,
            fdao,
        )
        return {
            "venta": venta.to_dict(),
            "detalle": detalle.to_dict(),
        }
    except ReferenciaUsuarioInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except ReferenciaDetalleInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except CodigoBoletoDuplicadoError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
    except AsientoOcupadoError as ex:
        raise HTTPException(status_code=409, detail=str(ex))


@router.put("/{venta_id}", response_model=VentaRespuesta)
def actualizar_venta(venta_id: int, datos: VentaActualizar):
    try:
        venta = dao.actualizar(venta_id, datos.id_usuario, datos.fecha_compra, udao)
        return venta.to_dict()
    except VentaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except ReferenciaUsuarioInvalidaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))


@router.delete("/{venta_id}")
def eliminar_venta(venta_id: int):
    try:
        dao.eliminar(venta_id)
        return {"mensaje": f"Venta ID={venta_id} eliminada"}
    except VentaNoEncontradaError as ex:
        raise HTTPException(status_code=404, detail=str(ex))
    except VentaConDetallesError as ex:
        raise HTTPException(status_code=409, detail=str(ex))
