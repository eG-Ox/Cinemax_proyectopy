# Semana 13 — Base de Datos SQLite y Relaciones

## Objetivo
Reemplazar la persistencia en archivos JSON por una base de datos relacional SQLite, agregando un nuevo modelo `Venta` con relaciones entre tablas (Foreign Keys).

## Qué cambió respecto a semana-12

| Archivo | Cambio |
|---|---|
| `config/base_datos.py` | **Nuevo** — conexión SQLite y creación de tablas |
| `dao/cliente_dao.py` | Reescrito para usar SQL en vez de listas |
| `dao/producto_dao.py` | Reescrito para usar SQL en vez de listas |
| `dao/venta_dao.py` | **Nuevo** — registrar y consultar ventas con JOIN |
| `modelos/venta.py` | **Nuevo** — modelo Venta |
| `main.py` | Llama a `inicializar()` al arrancar |
| `config/persistencia.py` | Ya no se usa (JSON reemplazado por SQLite) |

## Cómo ejecutar

> Requiere Python 3.10 o superior. SQLite viene incluido en Python, no necesitas instalar nada.

```bash
cd semana-13
python main.py
```

Al ejecutar, se crea automáticamente `sistema.db` en la misma carpeta.

---

## Archivo generado

```
semana-13/
└── sistema.db    ← base de datos SQLite (se crea al ejecutar)
```

Puedes abrirlo con [DB Browser for SQLite](https://sqlitebrowser.org/) para ver las tablas visualmente.

---

## Archivos clave explicados

### `config/base_datos.py` — Conexión y Schema
```python
import sqlite3

def obtener_conexion():
    conn = sqlite3.connect("sistema.db")
    conn.row_factory = sqlite3.Row   # permite acceder por nombre: fila["nombre"]
    return conn

def inicializar():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT    NOT NULL,
            ruc      TEXT    UNIQUE NOT NULL,
            ...
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id  INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            ...
            FOREIGN KEY (cliente_id)  REFERENCES clientes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)
    conn.commit()
    conn.close()
```

- `CREATE TABLE IF NOT EXISTS` — crea la tabla solo si no existe aún
- `AUTOINCREMENT` — el ID se asigna automáticamente
- `FOREIGN KEY` — garantiza integridad referencial (no puedes registrar una venta con un cliente que no existe)
- `conn.row_factory = sqlite3.Row` — convierte cada fila en un objeto que permite `fila["nombre"]` en vez de `fila[0]`

---

### `dao/cliente_dao.py` — DAO con SQL
El DAO ahora usa SQL puro en vez de listas:

```python
# ANTES (semana-11/12) — lista en RAM
def insertar(self, cliente):
    cliente.id = self.__cid
    self.__cid += 1
    self.__bd.append(cliente)

# AHORA (semana-13) — SQL
def insertar(self, cliente):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clientes (nombre, ruc, email, telefono) VALUES (?, ?, ?, ?)",
        (cliente.nombre, cliente.ruc, cliente.email, cliente.telefono)
    )
    conn.commit()
    cliente.id = cursor.lastrowid   # ID asignado por SQLite
    conn.close()
```

Los `?` son **placeholders** — evitan inyección SQL. Nunca uses f-strings para construir queries.

---

### `dao/venta_dao.py` — Consultas con JOIN
Las ventas relacionan clientes y productos usando JOIN:

```python
def obtener_todos(self):
    cursor.execute("""
        SELECT v.id,
               c.nombre AS cliente,    -- nombre del cliente, no el ID
               p.nombre AS producto,   -- nombre del producto, no el ID
               v.cantidad, v.fecha, v.total
        FROM ventas v
        JOIN clientes  c ON v.cliente_id  = c.id
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
    """)
```

El JOIN evita guardar el nombre del cliente dentro de la venta — solo guardamos el ID. Si el nombre del cliente cambia, la relación sigue siendo correcta.

---

### `modelos/venta.py` — Modelo con relaciones
```python
class Venta:
    def __init__(self, cliente_id, producto_id, cantidad):
        self.id          = None
        self.cliente_id  = cliente_id    # FK → clientes.id
        self.producto_id = producto_id   # FK → productos.id
        self.cantidad    = cantidad
        self.fecha       = None          # se asigna al registrar
        self.total       = 0.0           # se calcula al registrar
```

---

## Diagrama de tablas

```
clientes                productos
--------                ---------
id   (PK)               id   (PK)
nombre                  nombre
ruc  (UNIQUE)           precio
email
telefono
    ↑                       ↑
    |                       |
    └──── ventas ───────────┘
          id   (PK)
          cliente_id  (FK)
          producto_id (FK)
          cantidad
          fecha
          total
```

---

## Diferencia clave con JSON

| | JSON (semana-12) | SQLite (semana-13) |
|---|---|---|
| Búsqueda por campo | Recorre toda la lista | Índice automático en BD |
| Relaciones | No existen | Foreign Keys |
| Integridad | Manual | BD la garantiza |
| Múltiples usuarios | Conflictos | Manejado por SQLite |
| Visualización | Editor de texto | DB Browser, DBeaver |

---

## Ejercicio propuesto
1. Agrega un campo `stock` a la tabla `productos` (en `base_datos.py`)
2. Al registrar una venta, verifica que haya suficiente stock
3. Si hay stock, réstalo; si no, muestra un error apropiado
4. Agrega en el menú una opción para "Reponer stock" de un producto
