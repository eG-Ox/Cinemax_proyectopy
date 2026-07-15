from config.logger import Logger


class SistemaConfig:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.nombre = "Sistema de Gestion Cine"
            cls._instancia.version = "0.1"
            cls._instancia.empresa = "Proyecto Cine"
            cls._instancia.autor = "Proyecto personal"
            Logger().info(
                f"Sistema iniciado: {cls._instancia.nombre} "
                f"v{cls._instancia.version}"
            )
        return cls._instancia
