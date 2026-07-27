from config.logger import Logger


class UsuarioNoEncontradoError(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuario ID={usuario_id} no encontrado")


class CorreoDuplicadoError(Exception):
    def __init__(self, correo):
        super().__init__(f"Correo '{correo}' ya registrado")


class UsuarioDAO:
    def __init__(self):
        self.__bd = []
        self.__cid = 1
        self.__log = Logger()

    def buscar_por_correo(self, correo):
        for usuario in self.__bd:
            if usuario.correo == correo:
                return usuario
        return None

    def buscar_por_id(self, usuario_id):
        for usuario in self.__bd:
            if usuario.id == usuario_id:
                return usuario
        return None

    def insertar(self, usuario):
        if self.buscar_por_correo(usuario.correo):
            self.__log.warning(f"Correo duplicado: {usuario.correo}")
            raise CorreoDuplicadoError(usuario.correo)
        usuario.id = self.__cid
        self.__cid += 1
        self.__bd.append(usuario)
        self.__log.info(f"Usuario agregado: {usuario.nombres_usuario} (ID={usuario.id})")
        return usuario

    def obtener_todos(self):
        return sorted(self.__bd, key=lambda usuario: usuario.nombres_usuario)

    def actualizar(self, usuario_id, nombres_usuario=None, correo=None):
        usuario = self.buscar_por_id(usuario_id)
        if not usuario:
            self.__log.error(f"Actualizar fallido: Usuario ID={usuario_id} no existe")
            raise UsuarioNoEncontradoError(usuario_id)
        if correo and correo != usuario.correo:
            existente = self.buscar_por_correo(correo)
            if existente and existente.id != usuario_id:
                self.__log.warning(f"Correo duplicado en actualizacion: {correo}")
                raise CorreoDuplicadoError(correo)
        if nombres_usuario:
            usuario.nombres_usuario = nombres_usuario
        if correo:
            usuario.correo = correo
        self.__log.info(f"Usuario actualizado: ID={usuario_id}")
        return usuario

    def eliminar(self, usuario_id):
        usuario = self.buscar_por_id(usuario_id)
        if not usuario:
            self.__log.error(f"Eliminar fallido: Usuario ID={usuario_id} no existe")
            raise UsuarioNoEncontradoError(usuario_id)
        self.__bd.remove(usuario)
        self.__log.info(f"Usuario eliminado: {usuario.nombres_usuario} (ID={usuario_id})")
        return True

    def total(self):
        return len(self.__bd)
