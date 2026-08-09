from config.logger import Logger


class DetalleVentaNoEncontradoError(Exception):
    def __init__(self, detalle_id):
        super().__init__(f"Detalle de venta ID={detalle_id} no encontrado")


class ReferenciaDetalleInvalidaError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


class CodigoBoletoDuplicadoError(Exception):
    def __init__(self, codigo_boleto):
        super().__init__(f"Codigo de boleto '{codigo_boleto}' ya registrado")


class DetalleVentaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, detalle_id):
        for detalle in self.__bd:
            if detalle.id == detalle_id:
                return detalle
        return None

    def buscar_por_codigo(self, codigo_boleto):
        for detalle in self.__bd:
            if detalle.codigo_boleto == codigo_boleto:
                return detalle
        return None

    def insertar(self, detalle, venta_dao, funcion_dao):
        if self.buscar_por_codigo(detalle.codigo_boleto):
            self.__log.warning(f"Codigo de boleto duplicado: {detalle.codigo_boleto}")
            raise CodigoBoletoDuplicadoError(detalle.codigo_boleto)
        if not venta_dao.buscar_por_id(detalle.id_venta):
            self.__log.error(f"Detalle invalido: venta ID={detalle.id_venta} no existe")
            raise ReferenciaDetalleInvalidaError(f"Venta ID={detalle.id_venta} no encontrada")
        if not funcion_dao.buscar_por_id(detalle.id_funcion):
            self.__log.error(f"Detalle invalido: funcion ID={detalle.id_funcion} no existe")
            raise ReferenciaDetalleInvalidaError(f"Funcion ID={detalle.id_funcion} no encontrada")
        detalle.id = self.__cid
        self.__cid += 1
        self.__bd.append(detalle)
        self.__log.info(f"Detalle de venta agregado: ID={detalle.id}")
        return detalle

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda detalle: detalle.id)

    def actualizar(self, detalle_id, id_venta=None, id_funcion=None, asiento=None, codigo_boleto=None, venta_dao=None, funcion_dao=None):
        detalle = self.buscar_por_id(detalle_id)
        if not detalle:
            self.__log.error(f"Actualizar fallido: Detalle ID={detalle_id} no existe")
            raise DetalleVentaNoEncontradoError(detalle_id)
        if codigo_boleto and codigo_boleto != detalle.codigo_boleto:
            existente = self.buscar_por_codigo(codigo_boleto)
            if existente and existente.id != detalle_id:
                raise CodigoBoletoDuplicadoError(codigo_boleto)
        if id_venta is not None and venta_dao is not None:
            if not venta_dao.buscar_por_id(id_venta):
                raise ReferenciaDetalleInvalidaError(f"Venta ID={id_venta} no encontrada")
            detalle.id_venta = id_venta
        if id_funcion is not None and funcion_dao is not None:
            if not funcion_dao.buscar_por_id(id_funcion):
                raise ReferenciaDetalleInvalidaError(f"Funcion ID={id_funcion} no encontrada")
            detalle.id_funcion = id_funcion
        if asiento:
            detalle.asiento = asiento
        if codigo_boleto:
            detalle.codigo_boleto = codigo_boleto
        self.__log.info(f"Detalle de venta actualizado: ID={detalle_id}")
        return detalle

    def eliminar(self, detalle_id):
        detalle = self.buscar_por_id(detalle_id)
        if not detalle:
            self.__log.error(f"Eliminar fallido: Detalle ID={detalle_id} no existe")
            raise DetalleVentaNoEncontradoError(detalle_id)
        self.__bd.remove(detalle)
        self.__log.info(f"Detalle de venta eliminado: ID={detalle_id}")
        return True

    def total(self):
        return len(self.__bd)
