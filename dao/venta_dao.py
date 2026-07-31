from config.logger import Logger


class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")


class ReferenciaUsuarioInvalidaError(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuario ID={usuario_id} no encontrado")


class VentaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, venta_id):
        for venta in self.__bd:
            if venta.id == venta_id:
                return venta
        return None

    def insertar(self, venta, usuario_dao):
        if not usuario_dao.buscar_por_id(venta.id_usuario):
            self.__log.error(f"Venta invalida: usuario ID={venta.id_usuario} no existe")
            raise ReferenciaUsuarioInvalidaError(venta.id_usuario)
        venta.id = self.__cid
        self.__cid += 1
        self.__bd.append(venta)
        self.__log.info(f"Venta agregada: ID={venta.id}")
        return venta

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda venta: (venta.fecha_compra, venta.id))

    def actualizar(self, venta_id, id_usuario=None, fecha_compra=None, usuario_dao=None):
        venta = self.buscar_por_id(venta_id)
        if not venta:
            self.__log.error(f"Actualizar fallido: Venta ID={venta_id} no existe")
            raise VentaNoEncontradaError(venta_id)
        if id_usuario is not None and usuario_dao is not None:
            if not usuario_dao.buscar_por_id(id_usuario):
                raise ReferenciaUsuarioInvalidaError(id_usuario)
            venta.id_usuario = id_usuario
        if fecha_compra is not None:
            venta.fecha_compra = fecha_compra
        self.__log.info(f"Venta actualizada: ID={venta_id}")
        return venta

    def eliminar(self, venta_id):
        venta = self.buscar_por_id(venta_id)
        if not venta:
            self.__log.error(f"Eliminar fallido: Venta ID={venta_id} no existe")
            raise VentaNoEncontradaError(venta_id)
        self.__bd.remove(venta)
        self.__log.info(f"Venta eliminada: ID={venta_id}")
        return True

    def total(self):
        return len(self.__bd)
