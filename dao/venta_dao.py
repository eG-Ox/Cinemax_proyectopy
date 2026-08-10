import psycopg2
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.venta import Venta


class VentaNoEncontradaError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no encontrada")


class ReferenciaUsuarioInvalidaError(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuario ID={usuario_id} no encontrado")


class VentaConDetallesError(Exception):
    def __init__(self, venta_id):
        super().__init__(f"Venta ID={venta_id} no se puede eliminar: tiene detalles asociados")


class VentaDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_id(self, venta_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM venta WHERE id_venta = %s", (venta_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_venta(fila) if fila else None

    def insertar(self, venta, usuario_dao=None):
        if usuario_dao is not None and not usuario_dao.buscar_por_id(venta.id_usuario):
            self.__log.error(f"Venta invalida: usuario ID={venta.id_usuario} no existe")
            raise ReferenciaUsuarioInvalidaError(venta.id_usuario)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO venta (id_usuario, fecha_compra) VALUES (%s, %s) RETURNING id_venta",
                (venta.id_usuario, venta.fecha_compra),
            )
            venta.id = cursor.fetchone()["id_venta"]
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self.__log.error(f"Venta invalida: usuario ID={venta.id_usuario} no existe")
            raise ReferenciaUsuarioInvalidaError(venta.id_usuario)
        conn.close()
        self.__log.info(f"Venta agregada: ID={venta.id}")
        return venta

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM venta ORDER BY fecha_compra, id_venta")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_venta(fila) for fila in filas]

    def buscar_por_usuario(self, usuario_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM venta WHERE id_usuario = %s ORDER BY fecha_compra, id_venta",
            (usuario_id,),
        )
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_venta(fila) for fila in filas]

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
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE venta SET id_usuario=%s, fecha_compra=%s WHERE id_venta=%s",
                (venta.id_usuario, venta.fecha_compra, venta_id),
            )
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            raise ReferenciaUsuarioInvalidaError(venta.id_usuario)
        conn.close()
        self.__log.info(f"Venta actualizada: ID={venta_id}")
        return venta

    def eliminar(self, venta_id):
        venta = self.buscar_por_id(venta_id)
        if not venta:
            self.__log.error(f"Eliminar fallido: Venta ID={venta_id} no existe")
            raise VentaNoEncontradaError(venta_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM venta WHERE id_venta = %s", (venta_id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Venta ID={venta_id} tiene detalles asociados")
            raise VentaConDetallesError(venta_id)
        conn.close()
        self.__log.info(f"Venta eliminada: ID={venta_id}")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM venta")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_venta(self, fila):
        venta = Venta(fila["id_usuario"], fila["fecha_compra"])
        venta.id = fila["id_venta"]
        return venta
