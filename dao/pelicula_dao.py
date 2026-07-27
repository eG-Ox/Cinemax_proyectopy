from config.logger import Logger


class PeliculaNoEncontradaError(Exception):
    def __init__(self, pelicula_id):
        super().__init__(f"Pelicula ID={pelicula_id} no encontrada")


class PeliculaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, pelicula_id):
        for pelicula in self.__bd:
            if pelicula.id == pelicula_id:
                return pelicula
        return None

    def insertar(self, pelicula):
        pelicula.id = self.__cid
        self.__cid += 1
        self.__bd.append(pelicula)
        self.__log.info(f"Pelicula agregada: {pelicula.titulo} (ID={pelicula.id})")
        return pelicula

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda pelicula: pelicula.titulo)

    def actualizar(self, pelicula_id, titulo=None, genero=None, clasificacion=None, duracion=None):
        pelicula = self.buscar_por_id(pelicula_id)
        if not pelicula:
            self.__log.error(f"Actualizar fallido: Pelicula ID={pelicula_id} no existe")
            raise PeliculaNoEncontradaError(pelicula_id)
        if titulo:
            pelicula.titulo = titulo
        if genero:
            pelicula.genero = genero
        if clasificacion:
            pelicula.clasificacion = clasificacion
        if duracion is not None:
            pelicula.duracion = duracion
        self.__log.info(f"Pelicula actualizada: ID={pelicula_id}")
        return pelicula

    def eliminar(self, pelicula_id):
        pelicula = self.buscar_por_id(pelicula_id)
        if not pelicula:
            self.__log.error(f"Eliminar fallido: Pelicula ID={pelicula_id} no existe")
            raise PeliculaNoEncontradaError(pelicula_id)
        self.__bd.remove(pelicula)
        self.__log.info(f"Pelicula eliminada: {pelicula.titulo} (ID={pelicula_id})")
        return True

    def total(self):
        return len(self.__bd)
