class Sala:
    def __init__(self, id_pelicula, nombre_sala, capacidad, asientos_disponibles=None):
        self.id = None
        self.id_pelicula = id_pelicula
        self.nombre_sala = nombre_sala
        self.capacidad = capacidad
        self.asientos_disponibles = (
            capacidad if asientos_disponibles is None else asientos_disponibles
        )

    def __str__(self):
        return (
            f"[{self.id}] Pelicula={self.id_pelicula} | {self.nombre_sala} | "
            f"Capacidad: {self.capacidad} | Disponibles: {self.asientos_disponibles}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "id_pelicula": self.id_pelicula,
            "nombre_sala": self.nombre_sala,
            "capacidad": self.capacidad,
            "asientos_disponibles": self.asientos_disponibles,
        }

    @classmethod
    def from_dict(cls, datos):
        s = cls(
            datos.get("id_pelicula"),
            datos["nombre_sala"],
            datos["capacidad"],
            datos.get("asientos_disponibles"),
        )
        s.id = datos.get("id")
        return s
