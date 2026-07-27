class Sala:
    def __init__(self, nombre_sala, capacidad):
        self.id = None
        self.nombre_sala = nombre_sala
        self.capacidad = capacidad

    def __str__(self):
        return f"[{self.id}] {self.nombre_sala} | Capacidad: {self.capacidad}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre_sala": self.nombre_sala,
            "capacidad": self.capacidad,
        }

    @classmethod
    def from_dict(cls, datos):
        sala = cls(datos["nombre_sala"], datos["capacidad"])
        sala.id = datos.get("id")
        return sala
