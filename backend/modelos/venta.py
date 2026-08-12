from datetime import datetime


class Venta:
    def __init__(self, id_usuario, fecha_compra, total=0):
        self.id = None
        self.id_usuario = id_usuario
        self.fecha_compra = fecha_compra
        self.total = float(total)

    def __str__(self):
        return (
            f"[{self.id}] Usuario={self.id_usuario} | "
            f"{self.fecha_compra.strftime('%Y-%m-%d %H:%M:%S')} | Total={self.total:.2f}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "id_usuario": self.id_usuario,
            "fecha_compra": self.fecha_compra.isoformat(timespec="seconds"),
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, datos):
        v = cls(
            datos["id_usuario"],
            datetime.fromisoformat(datos["fecha_compra"]),
            datos.get("total", 0),
        )
        v.id = datos.get("id")
        return v
