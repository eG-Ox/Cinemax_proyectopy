import psycopg2
from config.base_datos import conexion_bd
from config.logger import Logger
from modelos.pelicula import Pelicula


class PeliculaNoEncontradaError(Exception):
    def __init__(self, pelicula_id):
        super().__init__(f"Pelicula ID={pelicula_id} no encontrada")


class PeliculaConFuncionesError(Exception):
    def __init__(self, pelicula_id):
        super().__init__(f"Pelicula ID={pelicula_id} no se puede eliminar: tiene funciones asociadas")


class PeliculaDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_id(self, pelicula_id):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pelicula WHERE id_pelicula = %s", (pelicula_id,))
            fila = cursor.fetchone()
        return self.__fila_a_pelicula(fila) if fila else None

    def insertar(self, pelicula):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO pelicula (titulo, genero, clasificacion, duracion)
                VALUES (%s, %s, %s, %s)
                RETURNING id_pelicula
                """,
                (pelicula.titulo, pelicula.genero, pelicula.clasificacion, pelicula.duracion),
            )
            pelicula.id = cursor.fetchone()["id_pelicula"]
            conn.commit()
        self.__log.info(f"Pelicula agregada: {pelicula.titulo} (ID={pelicula.id})")
        return pelicula

    def obtener_todos(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pelicula ORDER BY titulo")
            filas = cursor.fetchall()
        return [self.__fila_a_pelicula(fila) for fila in filas]

    def actualizar(self, pelicula_id, titulo=None, genero=None, clasificacion=None, duracion=None):
        pelicula = self.buscar_por_id(pelicula_id)
        if not pelicula:
            self.__log.error(f"Actualizar fallido: Pelicula ID={pelicula_id} no existe")
            raise PeliculaNoEncontradaError(pelicula_id)
        nuevo_titulo = titulo if titulo is not None else pelicula.titulo
        nuevo_genero = genero if genero is not None else pelicula.genero
        nueva_clasificacion = clasificacion if clasificacion is not None else pelicula.clasificacion
        nueva_duracion = duracion if duracion is not None else pelicula.duracion
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE pelicula
                SET titulo=%s, genero=%s, clasificacion=%s, duracion=%s
                WHERE id_pelicula=%s
                """,
                (nuevo_titulo, nuevo_genero, nueva_clasificacion, nueva_duracion, pelicula_id),
            )
            conn.commit()
        pelicula.titulo = nuevo_titulo
        pelicula.genero = nuevo_genero
        pelicula.clasificacion = nueva_clasificacion
        pelicula.duracion = nueva_duracion
        self.__log.info(f"Pelicula actualizada: ID={pelicula_id}")
        return pelicula

    def eliminar(self, pelicula_id):
        pelicula = self.buscar_por_id(pelicula_id)
        if not pelicula:
            self.__log.error(f"Eliminar fallido: Pelicula ID={pelicula_id} no existe")
            raise PeliculaNoEncontradaError(pelicula_id)
        with conexion_bd() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM pelicula WHERE id_pelicula = %s", (pelicula_id,))
                conn.commit()
            except psycopg2.IntegrityError:
                conn.rollback()
                self.__log.warning(f"Eliminar fallido: Pelicula ID={pelicula_id} tiene funciones asociadas")
                raise PeliculaConFuncionesError(pelicula_id)
        self.__log.info(f"Pelicula eliminada: {pelicula.titulo} (ID={pelicula_id})")
        return True

    def total(self):
        with conexion_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) AS total FROM pelicula")
            total = cursor.fetchone()["total"]
        return total

    def __fila_a_pelicula(self, fila):
        pelicula = Pelicula(
            fila["titulo"],
            fila["genero"],
            fila["clasificacion"],
            fila["duracion"],
        )
        pelicula.id = fila["id_pelicula"]
        return pelicula
