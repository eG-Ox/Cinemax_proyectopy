from datetime import date, time


class Funcion:
    def __init__(self, id_pelicula, id_sala, fecha_funcion, hora, precio):
        self.id = None
        self.id_pelicula = id_pelicula
        self.id_sala = id_sala
        self.fecha_funcion = fecha_funcion
        self.hora = hora
        self.precio = precio

    def __str__(self):
        return (
            f"[{self.id}] Pelicula={self.id_pelicula} | Sala={self.id_sala} | "
            f"{self.fecha_funcion.isoformat()} {self.hora.strftime('%H:%M')} | S/.{self.precio:.2f}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "id_pelicula": self.id_pelicula,
            "id_sala": self.id_sala,
            "fecha_funcion": self.fecha_funcion.isoformat(),
            "hora": self.hora.strftime("%H:%M:%S"),
            "precio": self.precio,
        }

    @classmethod
    def from_dict(cls, datos):
        funcion = cls(
            datos["id_pelicula"],
            datos["id_sala"],
            date.fromisoformat(datos["fecha_funcion"]),
            time.fromisoformat(datos["hora"]),
            datos["precio"],
        )
        funcion.id = datos.get("id")
        return funcion
