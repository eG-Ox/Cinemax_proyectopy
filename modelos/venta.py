from datetime import datetime


class Venta:
    def __init__(self, id_usuario, fecha_compra):
        self.id = None
        self.id_usuario = id_usuario
        self.fecha_compra = fecha_compra

    def __str__(self):
        return f"[{self.id}] Usuario={self.id_usuario} | {self.fecha_compra.strftime('%Y-%m-%d %H:%M:%S')}"

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "fecha_compra": self.fecha_compra.isoformat(timespec="seconds"),
        }

    @classmethod
    def from_dict(cls, datos):
        v = cls(datos["id_usuario"], datetime.fromisoformat(datos["fecha_compra"]))
        v.id = datos.get("id")
        return v
