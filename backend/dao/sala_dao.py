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


class SalaDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_id(self, sala_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sala WHERE id_sala = %s", (sala_id,))
            fila = cursor.fetchone()
        return self.__fila_a_sala(fila) if fila else None

    def insertar(self, sala):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sala (nombre_sala, capacidad) VALUES (%s, %s) RETURNING id_sala",
                (sala.nombre_sala, sala.capacidad),
            )
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

    def actualizar(self, sala_id, nombre_sala=None, capacidad=None):
        sala = self.buscar_por_id(sala_id)
        if not sala:
            self.__log.error(f"Actualizar fallido: Sala ID={sala_id} no existe")
            raise SalaNoEncontradaError(sala_id)
        nuevo_nombre = nombre_sala if nombre_sala is not None else sala.nombre_sala
        nueva_capacidad = capacidad if capacidad is not None else sala.capacidad
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE sala SET nombre_sala=%s, capacidad=%s WHERE id_sala=%s",
                (nuevo_nombre, nueva_capacidad, sala_id),
            )
            conn.commit()
        sala.nombre_sala = nuevo_nombre
        sala.capacidad = nueva_capacidad
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
        sala = Sala(fila["nombre_sala"], fila["capacidad"])
        sala.id = fila["id_sala"]
        return sala
