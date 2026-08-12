import psycopg2
from config.base_datos import conexion_bd
from config.logger import Logger
from modelos.sala import Sala


class SalaNoEncontradaError(Exception):
    def __init__(self, sala_id):
        super().__init__(f"Sala ID={sala_id} no encontrada")


class SalaConFuncionesError(Exception):
    def __init__(self, sala_id):
        super().__init__(f"Sala ID={sala_id} no se puede eliminar: tiene funciones asociadas")


class ReferenciaPeliculaSalaInvalidaError(Exception):
    def __init__(self, pelicula_id):
        super().__init__(f"Pelicula ID={pelicula_id} no encontrada")


class CapacidadSalaInsuficienteError(Exception):
    def __init__(self, sala_id, asientos_vendidos):
        super().__init__(
            f"Sala ID={sala_id} no puede tener menos de {asientos_vendidos} asientos"
        )


class SalaDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_id(self, sala_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sala WHERE id_sala = %s", (sala_id,))
            fila = cursor.fetchone()
        return self.__fila_a_sala(fila) if fila else None

    def insertar(self, sala, pelicula_dao=None):
        if pelicula_dao is not None and not pelicula_dao.buscar_por_id(sala.id_pelicula):
            self.__log.error(f"Sala invalida: pelicula ID={sala.id_pelicula} no existe")
            raise ReferenciaPeliculaSalaInvalidaError(sala.id_pelicula)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO sala (id_pelicula, nombre_sala, capacidad, asientos_disponibles)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_sala
                    """,
                    (
                        sala.id_pelicula,
                        sala.nombre_sala,
                        sala.capacidad,
                        sala.asientos_disponibles,
                    ),
                )
            except psycopg2.IntegrityError:
                conn.rollback()
                self.__log.error(f"Sala invalida: pelicula ID={sala.id_pelicula} no existe")
                raise ReferenciaPeliculaSalaInvalidaError(sala.id_pelicula)
            sala.id = cursor.fetchone()["id_sala"]
            conn.commit()
        self.__log.info(f"Sala agregada: {sala.nombre_sala} (ID={sala.id})")
        return sala

    def obtener_todos(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sala ORDER BY nombre_sala")
            filas = cursor.fetchall()
        return [self.__fila_a_sala(fila) for fila in filas]

    def buscar_por_pelicula(self, pelicula_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM sala WHERE id_pelicula = %s ORDER BY nombre_sala",
                (pelicula_id,),
            )
            filas = cursor.fetchall()
        return [self.__fila_a_sala(fila) for fila in filas]

    def actualizar(self, sala_id, id_pelicula=None, nombre_sala=None, capacidad=None, pelicula_dao=None):
        sala = self.buscar_por_id(sala_id)
        if not sala:
            self.__log.error(f"Actualizar fallido: Sala ID={sala_id} no existe")
            raise SalaNoEncontradaError(sala_id)
        nuevo_id_pelicula = id_pelicula if id_pelicula is not None else sala.id_pelicula
        if (
            id_pelicula is not None
            and pelicula_dao is not None
            and not pelicula_dao.buscar_por_id(id_pelicula)
        ):
            raise ReferenciaPeliculaSalaInvalidaError(id_pelicula)
        nuevo_nombre = nombre_sala if nombre_sala is not None else sala.nombre_sala
        nueva_capacidad = capacidad if capacidad is not None else sala.capacidad
        asientos_vendidos = max(sala.capacidad - sala.asientos_disponibles, 0)
        if capacidad is not None and nueva_capacidad < asientos_vendidos:
            raise CapacidadSalaInsuficienteError(sala_id, asientos_vendidos)
        nuevos_disponibles = (
            nueva_capacidad - asientos_vendidos
            if capacidad is not None
            else sala.asientos_disponibles
        )
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE sala
                    SET id_pelicula=%s, nombre_sala=%s, capacidad=%s, asientos_disponibles=%s
                    WHERE id_sala=%s
                    """,
                    (
                        nuevo_id_pelicula,
                        nuevo_nombre,
                        nueva_capacidad,
                        nuevos_disponibles,
                        sala_id,
                    ),
                )
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                raise ReferenciaPeliculaSalaInvalidaError(nuevo_id_pelicula)
        sala.id_pelicula = nuevo_id_pelicula
        sala.nombre_sala = nuevo_nombre
        sala.capacidad = nueva_capacidad
        sala.asientos_disponibles = nuevos_disponibles
        self.__log.info(f"Sala actualizada: ID={sala_id}")
        return sala

    def eliminar(self, sala_id):
        sala = self.buscar_por_id(sala_id)
        if not sala:
            self.__log.error(f"Eliminar fallido: Sala ID={sala_id} no existe")
            raise SalaNoEncontradaError(sala_id)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM sala WHERE id_sala = %s", (sala_id,))
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                self.__log.warning(f"Eliminar fallido: Sala ID={sala_id} tiene funciones asociadas")
                raise SalaConFuncionesError(sala_id)
        self.__log.info(f"Sala eliminada: {sala.nombre_sala} (ID={sala_id})")
        return True

    def total(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM sala")
            total = cursor.fetchone()["total"]
        return total

    def __fila_a_sala(self, fila):
        sala = Sala(
            fila.get("id_pelicula"),
            fila["nombre_sala"],
            fila["capacidad"],
            fila.get("asientos_disponibles", fila["capacidad"]),
        )
        sala.id = fila["id_sala"]
        return sala
