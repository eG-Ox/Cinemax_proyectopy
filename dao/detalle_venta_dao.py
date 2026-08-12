import psycopg2
from config.base_datos import conexion_bd
from config.logger import Logger
from modelos.detalle_venta import DetalleVenta


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
        self.__log = Logger()

    def buscar_por_id(self, detalle_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_venta WHERE id_detalle = %s", (detalle_id,))
            fila = cursor.fetchone()
        return self.__fila_a_detalle(fila) if fila else None

    def buscar_por_codigo(self, codigo_boleto):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_venta WHERE codigo_boleto = %s", (codigo_boleto,))
            fila = cursor.fetchone()
        return self.__fila_a_detalle(fila) if fila else None

    def insertar(self, detalle, venta_dao=None, funcion_dao=None):
        if self.buscar_por_codigo(detalle.codigo_boleto):
            self.__log.warning(f"Codigo de boleto duplicado: {detalle.codigo_boleto}")
            raise CodigoBoletoDuplicadoError(detalle.codigo_boleto)
        if venta_dao is not None and not venta_dao.buscar_por_id(detalle.id_venta):
            self.__log.error(f"Detalle invalido: venta ID={detalle.id_venta} no existe")
            raise ReferenciaDetalleInvalidaError(f"Venta ID={detalle.id_venta} no encontrada")
        if funcion_dao is not None and not funcion_dao.buscar_por_id(detalle.id_funcion):
            self.__log.error(f"Detalle invalido: funcion ID={detalle.id_funcion} no existe")
            raise ReferenciaDetalleInvalidaError(f"Funcion ID={detalle.id_funcion} no encontrada")
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO detalle_venta (id_venta, id_funcion, asiento, codigo_boleto)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_detalle
                    """,
                    (detalle.id_venta, detalle.id_funcion, detalle.asiento, detalle.codigo_boleto),
                )
                detalle.id = cursor.fetchone()["id_detalle"]
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ReferenciaDetalleInvalidaError("Venta o funcion no encontrada")
        self.__log.info(f"Detalle de venta agregado: ID={detalle.id}")
        return detalle

    def obtener_todos(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_venta ORDER BY id_detalle")
            filas = cursor.fetchall()
        return [self.__fila_a_detalle(fila) for fila in filas]

    def buscar_por_venta(self, venta_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM detalle_venta WHERE id_venta = %s ORDER BY id_detalle",
                (venta_id,),
            )
            filas = cursor.fetchall()
        return [self.__fila_a_detalle(fila) for fila in filas]

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
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE detalle_venta
                    SET id_venta=%s, id_funcion=%s, asiento=%s, codigo_boleto=%s
                    WHERE id_detalle=%s
                    """,
                    (
                        detalle.id_venta,
                        detalle.id_funcion,
                        detalle.asiento,
                        detalle.codigo_boleto,
                        detalle_id,
                    ),
                )
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ReferenciaDetalleInvalidaError("Venta o funcion no encontrada")
        self.__log.info(f"Detalle de venta actualizado: ID={detalle_id}")
        return detalle

    def eliminar(self, detalle_id):
        detalle = self.buscar_por_id(detalle_id)
        if not detalle:
            self.__log.error(f"Eliminar fallido: Detalle ID={detalle_id} no existe")
            raise DetalleVentaNoEncontradoError(detalle_id)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detalle_venta WHERE id_detalle = %s", (detalle_id,))
            conn.commit()
        self.__log.info(f"Detalle de venta eliminado: ID={detalle_id}")
        return True

    def total(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM detalle_venta")
            total = cursor.fetchone()["total"]
        return total

    def __fila_a_detalle(self, fila):
        detalle = DetalleVenta(
            fila["id_venta"],
            fila["id_funcion"],
            fila["asiento"],
            fila["codigo_boleto"],
        )
        detalle.id = fila["id_detalle"]
        return detalle
