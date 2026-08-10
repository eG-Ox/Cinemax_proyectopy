import psycopg2
from config.base_datos import obtener_conexion
from config.logger import Logger
from modelos.usuario import Usuario


class UsuarioNoEncontradoError(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuario ID={usuario_id} no encontrado")


class CorreoDuplicadoError(Exception):
    def __init__(self, correo):
        super().__init__(f"Correo '{correo}' ya registrado")


class UsuarioConVentasError(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuario ID={usuario_id} no se puede eliminar: tiene ventas asociadas")


class UsuarioDAO:
    def __init__(self):
        self.__log = Logger()

    def buscar_por_correo(self, correo):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE correo = %s", (correo,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_usuario(fila) if fila else None

    def buscar_por_id(self, usuario_id):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
        fila = cursor.fetchone()
        conn.close()
        return self.__fila_a_usuario(fila) if fila else None

    def insertar(self, usuario):
        if self.buscar_por_correo(usuario.correo):
            self.__log.warning(f"Correo duplicado: {usuario.correo}")
            raise CorreoDuplicadoError(usuario.correo)
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuario (nombres_usuario, correo) VALUES (%s, %s) RETURNING id_usuario",
            (usuario.nombres_usuario, usuario.correo),
        )
        usuario.id = cursor.fetchone()["id_usuario"]
        conn.commit()
        conn.close()
        self.__log.info(f"Usuario agregado: {usuario.nombres_usuario} (ID={usuario.id})")
        return usuario

    def obtener_todos(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario ORDER BY nombres_usuario")
        filas = cursor.fetchall()
        conn.close()
        return [self.__fila_a_usuario(fila) for fila in filas]

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
        nuevo_nombre = nombres_usuario if nombres_usuario is not None else usuario.nombres_usuario
        nuevo_correo = correo if correo is not None else usuario.correo
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET nombres_usuario=%s, correo=%s WHERE id_usuario=%s",
            (nuevo_nombre, nuevo_correo, usuario_id),
        )
        conn.commit()
        conn.close()
        usuario.nombres_usuario = nuevo_nombre
        usuario.correo = nuevo_correo
        self.__log.info(f"Usuario actualizado: ID={usuario_id}")
        return usuario

    def eliminar(self, usuario_id):
        usuario = self.buscar_por_id(usuario_id)
        if not usuario:
            self.__log.error(f"Eliminar fallido: Usuario ID={usuario_id} no existe")
            raise UsuarioNoEncontradoError(usuario_id)
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (usuario_id,))
            conn.commit()
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            self.__log.warning(f"Eliminar fallido: Usuario ID={usuario_id} tiene ventas asociadas")
            raise UsuarioConVentasError(usuario_id)
        conn.close()
        self.__log.info(f"Usuario eliminado: {usuario.nombres_usuario} (ID={usuario_id})")
        return True

    def total(self):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM usuario")
        total = cursor.fetchone()["total"]
        conn.close()
        return total

    def __fila_a_usuario(self, fila):
        usuario = Usuario(fila["nombres_usuario"], fila["correo"])
        usuario.id = fila["id_usuario"]
        return usuario
