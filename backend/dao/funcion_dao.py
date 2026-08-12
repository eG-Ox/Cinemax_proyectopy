import psycopg2
from config.base_datos import conexion_bd
from config.logger import Logger
from modelos.funcion import Funcion


class FuncionNoEncontradaError(Exception):
    def __init__(self, funcion_id):
        super().__init__(f"Funcion ID={funcion_id} no encontrada")


class ReferenciaInvalidaError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


class FuncionConDetallesError(Exception):
    def __init__(self, funcion_id):
        super().__init__(f"Funcion ID={funcion_id} no se puede eliminar: tiene detalles asociados")


class FuncionDAO:
    def __init__(self):
        self.__log = Logger()

    def __validar_sala_pelicula(self, sala, id_pelicula):
        if sala.id_pelicula is not None and sala.id_pelicula != id_pelicula:
            raise ReferenciaInvalidaError(
                f"Sala ID={sala.id} no esta asociada a la pelicula ID={id_pelicula}"
            )

    def buscar_por_id(self, funcion_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funcion WHERE id_funcion = %s", (funcion_id,))
            fila = cursor.fetchone()
        return self.__fila_a_funcion(fila) if fila else None

    def insertar(self, funcion, pelicula_dao, sala_dao):
        if pelicula_dao is not None and not pelicula_dao.buscar_por_id(funcion.id_pelicula):
            self.__log.error(f"Funcion invalida: pelicula ID={funcion.id_pelicula} no existe")
            raise ReferenciaInvalidaError(f"Pelicula ID={funcion.id_pelicula} no encontrada")
        if sala_dao is not None:
            sala = sala_dao.buscar_por_id(funcion.id_sala)
            if not sala:
                self.__log.error(f"Funcion invalida: sala ID={funcion.id_sala} no existe")
                raise ReferenciaInvalidaError(f"Sala ID={funcion.id_sala} no encontrada")
            self.__validar_sala_pelicula(sala, funcion.id_pelicula)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO funcion (id_pelicula, id_sala, fecha_funcion, hora, precio)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_funcion
                    """,
                    (
                        funcion.id_pelicula,
                        funcion.id_sala,
                        funcion.fecha_funcion,
                        funcion.hora,
                        funcion.precio,
                    ),
                )
                funcion.id = cursor.fetchone()["id_funcion"]
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ReferenciaInvalidaError("Pelicula o sala no encontrada")
        self.__log.info(f"Funcion agregada: ID={funcion.id}")
        return funcion

    def obtener_todos(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM funcion ORDER BY fecha_funcion, hora, id_funcion")
            filas = cursor.fetchall()
        return [self.__fila_a_funcion(fila) for fila in filas]

    def actualizar(self, funcion_id, id_pelicula=None, id_sala=None, fecha_funcion=None, hora=None, precio=None, pelicula_dao=None, sala_dao=None):
        funcion = self.buscar_por_id(funcion_id)
        if not funcion:
            self.__log.error(f"Actualizar fallido: Funcion ID={funcion_id} no existe")
            raise FuncionNoEncontradaError(funcion_id)
        if id_pelicula is not None and pelicula_dao is not None:
            if not pelicula_dao.buscar_por_id(id_pelicula):
                raise ReferenciaInvalidaError(f"Pelicula ID={id_pelicula} no encontrada")
            funcion.id_pelicula = id_pelicula
        if id_sala is not None and sala_dao is not None:
            if not sala_dao.buscar_por_id(id_sala):
                raise ReferenciaInvalidaError(f"Sala ID={id_sala} no encontrada")
            funcion.id_sala = id_sala
        if fecha_funcion is not None:
            funcion.fecha_funcion = fecha_funcion
        if hora is not None:
            funcion.hora = hora
        if precio is not None:
            funcion.precio = precio
        if sala_dao is not None:
            sala = sala_dao.buscar_por_id(funcion.id_sala)
            if not sala:
                raise ReferenciaInvalidaError(f"Sala ID={funcion.id_sala} no encontrada")
            self.__validar_sala_pelicula(sala, funcion.id_pelicula)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE funcion
                    SET id_pelicula=%s, id_sala=%s, fecha_funcion=%s, hora=%s, precio=%s
                    WHERE id_funcion=%s
                    """,
                    (
                        funcion.id_pelicula,
                        funcion.id_sala,
                        funcion.fecha_funcion,
                        funcion.hora,
                        funcion.precio,
                        funcion_id,
                    ),
                )
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ReferenciaInvalidaError("Pelicula o sala no encontrada")
        self.__log.info(f"Funcion actualizada: ID={funcion_id}")
        return funcion

    def eliminar(self, funcion_id):
        funcion = self.buscar_por_id(funcion_id)
        if not funcion:
            self.__log.error(f"Eliminar fallido: Funcion ID={funcion_id} no existe")
            raise FuncionNoEncontradaError(funcion_id)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM funcion WHERE id_funcion = %s", (funcion_id,))
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                self.__log.warning(f"Eliminar fallido: Funcion ID={funcion_id} tiene detalles asociados")
                raise FuncionConDetallesError(funcion_id)
        self.__log.info(f"Funcion eliminada: ID={funcion_id}")
        return True

    def total(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM funcion")
            total = cursor.fetchone()["total"]
        return total

    def __fila_a_funcion(self, fila):
        funcion = Funcion(
            fila["id_pelicula"],
            fila["id_sala"],
            fila["fecha_funcion"],
            fila["hora"],
            float(fila["precio"]),
        )
        funcion.id = fila["id_funcion"]
        return funcion
