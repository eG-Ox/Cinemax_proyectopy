class DetalleVenta:
    def __init__(self, id_venta, id_funcion, asiento, codigo_boleto):
        self.id = None
        self.id_venta = id_venta
        self.id_funcion = id_funcion
        self.asiento = asiento
        self.codigo_boleto = codigo_boleto

    def __str__(self):
        return (
            f"[{self.id}] Venta={self.id_venta} | Funcion={self.id_funcion} | "
            f"Asiento={self.asiento} | Boleto={self.codigo_boleto}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "id_venta": self.id_venta,
            "id_funcion": self.id_funcion,
            "asiento": self.asiento,
            "codigo_boleto": self.codigo_boleto,
        }

    @classmethod
    def from_dict(cls, datos):
        d = cls(
            datos["id_venta"],
            datos["id_funcion"],
            datos["asiento"],
            datos["codigo_boleto"],
        )
        d.id = datos.get("id")
        return d
