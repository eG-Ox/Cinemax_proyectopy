from config.logger import Logger


class UsuarioDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def insertar(self, usuario):
        usuario.id = self.__cid
        self.__cid += 1
        self.__bd.append(usuario)
        self.__log.info(f"Usuario agregado: {usuario.nombres_usuario}")
        return usuario

    def obtener_todos(self):
        return list(self.__bd)
