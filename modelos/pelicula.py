class Pelicula:
    def __init__(self, titulo, genero, clasificacion, duracion):
        self.id = None
        self.titulo = titulo
        self.genero = genero
        self.clasificacion = clasificacion
        self.duracion = duracion

    def __str__(self):
        return (
            f"[{self.id}] {self.titulo} | {self.genero} | "
            f"{self.clasificacion} | {self.duracion} min"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "genero": self.genero,
            "clasificacion": self.clasificacion,
            "duracion": self.duracion,
        }

    @classmethod
    def from_dict(cls, datos):
        pelicula = cls(
            datos["titulo"],
            datos["genero"],
            datos["clasificacion"],
            datos["duracion"],
        )
        pelicula.id = datos.get("id")
        return pelicula
