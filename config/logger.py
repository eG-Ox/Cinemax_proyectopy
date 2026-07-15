class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._mensajes = []
        return cls._instancia

    def info(self, mensaje):
        self._mensajes.append(("INFO", mensaje))

    def warning(self, mensaje):
        self._mensajes.append(("WARNING", mensaje))

    def error(self, mensaje):
        self._mensajes.append(("ERROR", mensaje))

    def mostrar_logs(self):
        print(f"\n=== LOGS ({len(self._mensajes)} eventos) ===")
        for nivel, mensaje in self._mensajes:
            print(f" {nivel:7} | {mensaje}")

    def limpiar(self):
        self._mensajes.clear()
class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._mensajes = []
        return cls._instancia

    def info(self, mensaje):
        self._mensajes.append(("INFO", mensaje))

    def warning(self, mensaje):
        self._mensajes.append(("WARNING", mensaje))

    def error(self, mensaje):
        self._mensajes.append(("ERROR", mensaje))

    def mostrar_logs(self):
        print(f"\n=== LOGS ({len(self._mensajes)} eventos) ===")
        for nivel, mensaje in self._mensajes:
            print(f" {nivel:7} | {mensaje}")

    def limpiar(self):
        self._mensajes.clear()
