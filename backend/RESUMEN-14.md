# Semana 14 — API REST con FastAPI y PostgreSQL

## Objetivo
Convertir el sistema CLI en una **API REST** consumible desde cualquier frontend (React, móvil, Postman), usando FastAPI y reemplazando SQLite por PostgreSQL.

## Qué cambió respecto a semana-13

| Archivo | Cambio |
|---|---|
| `main.py` | De menú CLI a aplicación FastAPI |
| `config/base_datos.py` | De `sqlite3` a `psycopg2` (PostgreSQL) |
| `routers/` | **Nuevo** — endpoints HTTP por recurso |
| `schemas/` | **Nuevo** — validación de datos con Pydantic |
| `dao/` | Solo cambio de `?` por `%s` y `RETURNING id` |
| `modelos/` | Sin cambios |
| `vistas/menu.py` | Ya no se usa (era de semana-13) |

## Requisitos previos

```bash
pip install fastapi uvicorn psycopg2-binary
```

Además necesitas PostgreSQL instalado y corriendo con una base de datos creada:

```sql
CREATE DATABASE sistema_db;
```

## Cómo ejecutar

La API necesita conectarse a PostgreSQL. La contraseña se pasa como variable de entorno.

**En Windows PowerShell** (todo en una sola línea):

```powershell
$env:DB_PASSWORD = "admin123"; uvicorn main:app --reload
```

> Reemplaza `admin123` por la contraseña que pusiste al instalar PostgreSQL.

**¿Por qué usamos `$env:DB_PASSWORD`?**
- `$env:NOMBRE = "valor"` define una variable de entorno en PowerShell
- El código la lee con `os.getenv("DB_PASSWORD")` — así la contraseña no queda escrita en el código fuente
- El `;` encadena dos comandos: primero define la variable, luego ejecuta uvicorn

**¿Por qué no funciona solo `uvicorn main:app --reload`?**
- PostgreSQL requiere contraseña para conectarse
- Si no se define `DB_PASSWORD`, el valor por defecto es vacío `""` y PostgreSQL rechaza la conexión

Luego abre en el navegador:
- **`http://localhost:8000/docs`** — Swagger UI (documentación interactiva automática)
- **`http://localhost:8000`** — endpoint raíz

### Variables de entorno disponibles

```powershell
# Si tu PostgreSQL usa configuración distinta, ajusta estas variables:
$env:DB_HOST     = "localhost"   # servidor (por defecto: localhost)
$env:DB_PORT     = "5432"        # puerto    (por defecto: 5432)
$env:DB_NAME     = "sistema_db"  # base de datos
$env:DB_USER     = "postgres"    # usuario
$env:DB_PASSWORD = "admin123"    # contraseña
```

---

## Estructura nueva

```
semana-14/
├── main.py               ← crea la app FastAPI y registra routers
├── config/
│   └── base_datos.py     ← conexión PostgreSQL con psycopg2
├── routers/
│   ├── clientes.py       ← endpoints GET/POST/PUT/DELETE /clientes
│   ├── productos.py      ← endpoints GET/POST/PUT/DELETE /productos
│   └── ventas.py         ← endpoints GET/POST /ventas
├── schemas/
│   ├── cliente_schema.py ← modelos Pydantic para clientes
│   ├── producto_schema.py← modelos Pydantic para productos
│   └── venta_schema.py   ← modelos Pydantic para ventas
├── dao/                  ← igual que semana-13 (solo %s en vez de ?)
└── modelos/              ← sin cambios
```

---

## Archivos clave explicados

### `main.py` — Aplicación FastAPI
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sistema de Gestión POO")

# Permite que React en localhost consuma la API
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()                    # crea las tablas si no existen
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(ventas.router)
```

---

### `schemas/cliente_schema.py` — Validación con Pydantic
```python
from pydantic import BaseModel
from typing import Optional

class ClienteCrear(BaseModel):      # lo que llega en el body del POST
    nombre:   str
    ruc:      str
    email:    str
    telefono: str

class ClienteActualizar(BaseModel): # body del PUT (todos opcionales)
    nombre:   Optional[str] = None
    email:    Optional[str] = None
    telefono: Optional[str] = None

class ClienteRespuesta(BaseModel):  # lo que devuelve la API
    id:       int
    nombre:   str
    ruc:      str
    email:    str
    telefono: str
```

**Por qué tres schemas separados?**
- Al **crear** no envías `id` (lo genera la BD)
- Al **actualizar** todos los campos son opcionales
- Al **responder** siempre incluyes `id`

---

### `routers/clientes.py` — Endpoints HTTP
```python
router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[ClienteRespuesta])
def listar_clientes():
    return [c.to_dict() for c in dao.obtener_todos()]

@router.get("/{cliente_id}", response_model=ClienteRespuesta)
def obtener_cliente(cliente_id: int):
    c = dao.buscar_por_id(cliente_id)
    if not c:
        raise HTTPException(status_code=404, detail="No encontrado")
    return c.to_dict()

@router.post("/", response_model=ClienteRespuesta, status_code=201)
def crear_cliente(datos: ClienteCrear):
    try:
        c = dao.insertar(Cliente(datos.nombre, datos.ruc, datos.email, datos.telefono))
        return c.to_dict()
    except RUCDuplicadoError as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.put("/{cliente_id}", response_model=ClienteRespuesta)
def actualizar_cliente(cliente_id: int, datos: ClienteActualizar): ...

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int): ...
```

---

## Endpoints disponibles

| Método | URL | Qué hace |
|---|---|---|
| GET | `/clientes` | Lista todos los clientes |
| GET | `/clientes/{id}` | Obtiene un cliente por ID |
| POST | `/clientes` | Crea un cliente nuevo |
| PUT | `/clientes/{id}` | Actualiza un cliente |
| DELETE | `/clientes/{id}` | Elimina un cliente |
| GET | `/productos` | Lista todos los productos |
| GET | `/productos/{id}` | Obtiene un producto por ID |
| POST | `/productos` | Crea un producto nuevo |
| PUT | `/productos/{id}` | Actualiza un producto |
| DELETE | `/productos/{id}` | Elimina un producto |
| GET | `/ventas` | Lista todas las ventas |
| GET | `/ventas/{id}` | Obtiene una venta por ID |
| POST | `/ventas` | Registra una venta nueva |
| GET | `/ventas/cliente/{id}` | Ventas de un cliente específico |

---

## Probar la API con Postman o curl

```bash
# Crear cliente
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana García","ruc":"20111222333","email":"ana@mail.com","telefono":"999888777"}'

# Listar clientes
curl http://localhost:8000/clientes

# Eliminar cliente con ID=1
curl -X DELETE http://localhost:8000/clientes/1
```

O simplemente abre `http://localhost:8000/docs` y prueba todo desde el navegador.

---

## Diferencia con semana-13

| | semana-13 | semana-14 |
|---|---|---|
| Interfaz | Terminal (input/print) | HTTP (JSON) |
| Consume desde | Solo la PC local | Cualquier cliente HTTP |
| Documentación | El menú impreso | Swagger en `/docs` |
| BD | SQLite (archivo local) | PostgreSQL (servidor) |
| Validación | Manual con try/except | Pydantic automático |
| Errores | print("ERROR:...") | HTTP 400, 404, 500 |

---

## Ejercicio propuesto
1. Agrega en `schemas/cliente_schema.py` validación de email con `pydantic.EmailStr`
2. Agrega un endpoint `GET /ventas/resumen` que devuelva el total de ventas y la suma total de dinero
3. Prueba todos los endpoints desde Swagger (`/docs`) y anota qué código HTTP devuelve cada caso de error
