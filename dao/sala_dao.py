from config.logger import Logger


class SalaNoEncontradaError(Exception):
    def __init__(self, sala_id):
        super().__init__(f"Sala ID={sala_id} no encontrada")


class SalaDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_id(self, sala_id):
        for sala in self.__bd:
            if sala.id == sala_id:
                return sala
        return None

    def insertar(self, sala):
        sala.id = self.__cid
        self.__cid += 1
        self.__bd.append(sala)
        self.__log.info(f"Sala agregada: {sala.nombre_sala} (ID={sala.id})")
        return sala

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda sala: sala.nombre_sala)

    def actualizar(self, sala_id, nombre_sala=None, capacidad=None):
        sala = self.buscar_por_id(sala_id)
        if not sala:
            self.__log.error(f"Actualizar fallido: Sala ID={sala_id} no existe")
            raise SalaNoEncontradaError(sala_id)
        if nombre_sala:
            sala.nombre_sala = nombre_sala
        if capacidad is not None:
            sala.capacidad = capacidad
        self.__log.info(f"Sala actualizada: ID={sala_id}")
        return sala

    def eliminar(self, sala_id):
        sala = self.buscar_por_id(sala_id)
        if not sala:
            self.__log.error(f"Eliminar fallido: Sala ID={sala_id} no existe")
            raise SalaNoEncontradaError(sala_id)
        self.__bd.remove(sala)
        self.__log.info(f"Sala eliminada: {sala.nombre_sala} (ID={sala_id})")
        return True

    def total(self):
        return len(self.__bd)
