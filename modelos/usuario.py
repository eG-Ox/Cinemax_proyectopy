class Usuario:
    def __init__(self, nombres_usuario, correo):
        self.id = None
        self.nombres_usuario = nombres_usuario
        self.correo = correo

    def __str__(self):
        return f"[{self.id}] {self.nombres_usuario} | {self.correo}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombres_usuario": self.nombres_usuario,
            "correo": self.correo,
        }

    @classmethod
    def from_dict(cls, datos):
        usuario = cls(datos["nombres_usuario"], datos["correo"])
        usuario.id = datos.get("id")
        return usuario
