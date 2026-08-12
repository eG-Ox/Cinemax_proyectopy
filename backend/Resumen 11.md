# Semana 11 — Modularización y Patrón DAO

## Objetivo
Separar un programa monolítico en módulos con responsabilidades claras, aplicando los patrones de diseño **Singleton** y **DAO** (Data Access Object).

## Qué cambió respecto al ejercicio anterior
El archivo único `ejercicioDAOSingleton.py` se dividió en carpetas y archivos especializados. El código hace exactamente lo mismo, pero ahora cada parte tiene su propio lugar.

```
semana-11/
├── main.py               ← punto de entrada, orquesta todo
├── config/
│   ├── logger.py         ← registro de eventos (Singleton)
│   └── sistema_config.py ← configuración global (Singleton)
├── modelos/
│   ├── cliente.py        ← clase Cliente (solo datos)
│   └── producto.py       ← clase Producto (solo datos)
├── dao/
│   ├── cliente_dao.py    ← CRUD de clientes en memoria
│   └── producto_dao.py   ← CRUD de productos en memoria
└── vistas/
    └── menu.py           ← funciones de pantalla e inputs
```

## Cómo ejecutar

> Requiere Python 3.10 o superior (usa `match`/`case`)

```bash
cd semana-11
python main.py
```

No necesita instalar ninguna librería externa.

---

## Archivos clave explicados

### `config/logger.py` — Patrón Singleton
```python
class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:          # solo crea el objeto la primera vez
            cls._instancia = super().__new__(cls)
            cls._instancia._logs = []
        return cls._instancia               # siempre devuelve la MISMA instancia
```
**Por qué Singleton?** El historial de logs debe ser uno solo en todo el sistema. Si cada parte del programa creara su propio Logger, habría múltiples listas de logs separadas y se perdería el registro completo.

---

### `modelos/cliente.py` — Modelo puro
```python
class Cliente:
    def __init__(self, nombre, ruc, email, telefono):
        self.id       = None
        self.nombre   = nombre
        self.ruc      = ruc
        self.email    = email
        self.telefono = telefono
```
El modelo solo **representa datos**. No sabe cómo guardarse, ni cómo mostrarse en pantalla. Esa separación es intencional.

---

### `dao/cliente_dao.py` — Patrón DAO
```python
class ClienteDAO:
    def __init__(self):
        self.__bd  = []   # lista privada = "base de datos" en memoria
        self.__cid = 1    # contador de IDs

    def insertar(self, cliente): ...
    def buscar_por_id(self, id): ...
    def obtener_todos(self):     ...
    def actualizar(self, id):    ...
    def eliminar(self, id):      ...
```
**Por qué DAO?** Toda la lógica de almacenamiento queda en un solo lugar. Si mañana cambiamos de lista en memoria a una base de datos real, solo modificamos este archivo. `main.py`, `menu.py` y los modelos no se tocan.

---

### `vistas/menu.py` — Capa de presentación
Contiene funciones que muestran pantallas y reciben inputs del usuario. No contiene lógica de negocio. Recibe el DAO como parámetro y lo usa.

```python
def agregar_cliente(cdao):          # recibe el DAO, no lo crea
    nombre = input("Nombre: ")
    c = cdao.insertar(Cliente(...))  # delega al DAO
```

---

### `main.py` — Orquestador
Crea los objetos necesarios y conecta las capas entre sí usando `match`/`case` de Python 3.10:

```python
cfg  = SistemaConfig()   # configuración global
cdao = ClienteDAO()      # acceso a datos de clientes
pdao = ProductoDAO()     # acceso a datos de productos

match opcion:
    case "1": agregar_cliente(cdao)
    case "2": agregar_producto(pdao)
    ...
```

---

## Limitación de esta versión
Los datos viven en RAM. Al cerrar el programa con opción `0`, **todo se pierde**. Eso se resuelve en la siguiente semana.

---

## Ejercicio propuesto
1. Agrega un campo `categoria` a la clase `Producto` (ej: "electronico", "ropa", "alimento")
2. Agrega en `ProductoDAO` un método `buscar_por_categoria(categoria)` que filtre la lista
3. Agrega la opción 11 en el menú que llame a ese nuevo método
