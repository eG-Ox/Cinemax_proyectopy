from config.logger import Logger


class FuncionNoEncontradaError(Exception):
    def __init__(self, funcion_id):
        super().__init__(f"Funcion ID={funcion_id} no encontrada")


class ReferenciaInvalidaError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)


class FuncionDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, funcion_id):
        for funcion in self.__bd:
            if funcion.id == funcion_id:
                return funcion
        return None

    def insertar(self, funcion, pelicula_dao, sala_dao):
        if not pelicula_dao.buscar_por_id(funcion.id_pelicula):
            self.__log.error(f"Funcion invalida: pelicula ID={funcion.id_pelicula} no existe")
            raise ReferenciaInvalidaError(f"Pelicula ID={funcion.id_pelicula} no encontrada")
        if not sala_dao.buscar_por_id(funcion.id_sala):
            self.__log.error(f"Funcion invalida: sala ID={funcion.id_sala} no existe")
            raise ReferenciaInvalidaError(f"Sala ID={funcion.id_sala} no encontrada")
        funcion.id = self.__cid
        self.__cid += 1
        self.__bd.append(funcion)
        self.__log.info(f"Funcion agregada: ID={funcion.id}")
        return funcion

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda funcion: (funcion.fecha_funcion, funcion.hora, funcion.id))

    def actualizar(
        self,
        funcion_id,
        id_pelicula=None,
        id_sala=None,
        fecha_funcion=None,
        hora=None,
        precio=None,
        pelicula_dao=None,
        sala_dao=None,
    ):
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
        self.__log.info(f"Funcion actualizada: ID={funcion_id}")
        return funcion

    def eliminar(self, funcion_id):
        funcion = self.buscar_por_id(funcion_id)
        if not funcion:
            self.__log.error(f"Eliminar fallido: Funcion ID={funcion_id} no existe")
            raise FuncionNoEncontradaError(funcion_id)
        self.__bd.remove(funcion)
        self.__log.info(f"Funcion eliminada: ID={funcion_id}")
        return True

    def total(self):
        return len(self.__bd)
