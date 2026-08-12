# CINEMAX - API REST

## Descripcion

API REST desarrollada con FastAPI para el sistema de gestion de cine Cinemax.

La API permite gestionar usuarios, peliculas, salas, funciones, ventas y detalles de venta.

La aplicacion utiliza PostgreSQL como base de datos y sigue una estructura separada por modelos, schemas, DAO y routers.

---

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- PostgreSQL
- psycopg2
- Uvicorn

---

## Requisitos

Antes de ejecutar la API se necesita tener instalado:

- Python
- PostgreSQL
- pip
- Uvicorn

Tambien se debe tener disponible una base de datos PostgreSQL para el sistema.

---

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/eG-Ox/Cinemax_proyectopy
```

### 2. Entrar a la carpeta de la API

```bash
cd Cinemax_proyectopy
```

### 3. Instalar las dependencias

```bash
pip install fastapi uvicorn psycopg2-binary pydantic
```

---

## Configuracion de PostgreSQL

La conexion con PostgreSQL se encuentra en:

```text
config/base_datos.py
```

La API utiliza los siguientes valores de configuracion:

```text
Host: localhost
Puerto: 5432
Base de datos: cine
Usuario: postgres
Contrasena: ""
```

Estos valores pueden ser modificados mediante las siguientes variables de entorno:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
```

La base de datos debe estar creada y PostgreSQL debe encontrarse ejecutandose antes de iniciar la API.

```sql
CREATE DATABASE cine;
```

---

## Base de datos

Al iniciar la aplicacion se ejecuta la funcion `inicializar()` de:

```text
config/base_datos.py
```

Esta funcion crea las tablas necesarias si todavia no existen.

### Tablas principales

#### Usuario

- `id_usuario`
- `nombres_usuario`
- `correo`

#### Pelicula

- `id_pelicula`
- `titulo`
- `genero`
- `clasificacion`
- `duracion`

#### Sala

- `id_sala`
- `nombre_sala`
- `capacidad`

#### Funcion

- `id_funcion`
- `id_pelicula`
- `id_sala`
- `fecha_funcion`
- `hora`
- `precio`

#### Venta

- `id_venta`
- `id_usuario`
- `fecha_compra`

#### Detalle de venta

- `id_detalle`
- `id_venta`
- `id_funcion`
- `asiento`
- `codigo_boleto`

Las tablas `funcion`, `venta` y `detalle_venta` mantienen relaciones mediante claves foraneas.

---

## Ejecucion

Para iniciar la API con Uvicorn:

```bash
uvicorn main:app --reload
```

En Windows PowerShell, si PostgreSQL requiere contrasena:

```powershell
$env:DB_PASSWORD = "admin123"; uvicorn main:app --reload
```

La API estara disponible normalmente en:

```text
http://localhost:8000
```

---

## Documentacion de la API

FastAPI genera automaticamente la documentacion interactiva.

### Swagger UI

```text
http://localhost:8000/docs
```

### Documentacion alternativa

```text
http://localhost:8000/redoc
```

---

## Endpoint principal

### Inicio

```http
GET /
```

Devuelve informacion basica de la API:

```json
{
    "mensaje": "API Sistema de Gestion de Cine Cinemax",
    "version": "1.0",
    "docs": "/docs"
}
```

---

# Endpoints

## Usuarios

Ruta base:

```text
/usuarios
```

- `GET /usuarios/`
- `GET /usuarios/{usuario_id}`
- `POST /usuarios/`
- `PUT /usuarios/{usuario_id}`
- `DELETE /usuarios/{usuario_id}`

Ejemplo para registrar usuario:

```json
{
    "nombres_usuario": "Marco Minanoh",
    "correo": "marco@mail.com"
}
```

## Peliculas

Ruta base:

```text
/peliculas
```

- `GET /peliculas/`
- `GET /peliculas/{pelicula_id}`
- `POST /peliculas/`
- `PUT /peliculas/{pelicula_id}`
- `DELETE /peliculas/{pelicula_id}`

Ejemplo:

```json
{
    "titulo": "Interestelar",
    "genero": "Ciencia ficcion",
    "clasificacion": "PG-13",
    "duracion": 169
}
```

## Salas

Ruta base:

```text
/salas
```

- `GET /salas/`
- `GET /salas/{sala_id}`
- `POST /salas/`
- `PUT /salas/{sala_id}`
- `DELETE /salas/{sala_id}`

Ejemplo:

```json
{
    "nombre_sala": "Sala 1",
    "capacidad": 120
}
```

## Funciones

Ruta base:

```text
/funciones
```

- `GET /funciones/`
- `GET /funciones/{funcion_id}`
- `POST /funciones/`
- `PUT /funciones/{funcion_id}`
- `DELETE /funciones/{funcion_id}`

Ejemplo:

```json
{
    "id_pelicula": 1,
    "id_sala": 1,
    "fecha_funcion": "2026-08-10",
    "hora": "20:30:00",
    "precio": 18.50
}
```

## Ventas

Ruta base:

```text
/ventas
```

- `GET /ventas/`
- `GET /ventas/{venta_id}`
- `GET /ventas/usuario/{usuario_id}`
- `POST /ventas/`
- `PUT /ventas/{venta_id}`
- `DELETE /ventas/{venta_id}`

Ejemplo:

```json
{
    "id_usuario": 1
}
```

## Detalles de venta

Ruta base:

```text
/detalles-venta
```

- `GET /detalles-venta/`
- `GET /detalles-venta/{detalle_id}`
- `GET /detalles-venta/venta/{venta_id}`
- `POST /detalles-venta/`
- `PUT /detalles-venta/{detalle_id}`
- `DELETE /detalles-venta/{detalle_id}`

Ejemplo:

```json
{
    "id_venta": 1,
    "id_funcion": 1,
    "asiento": "A1",
    "codigo_boleto": "BOL-001"
}
```

## Registros

Ruta base:

```text
/registros
```

- `GET /registros/`
- `DELETE /registros/`

---

# Validaciones

La API utiliza Pydantic mediante los archivos de `schemas/` para validar los datos recibidos.

### Peliculas

- La duracion debe ser mayor que cero.

### Salas

- La capacidad debe ser mayor que cero.

### Funciones

- El precio debe ser mayor que cero.
- La pelicula debe existir.
- La sala debe existir.

### Ventas

- El usuario debe existir.

### Detalles de venta

- La venta debe existir.
- La funcion debe existir.
- No se permite registrar un codigo de boleto duplicado.

---

# Manejo de errores

La API utiliza excepciones personalizadas y `HTTPException` para informar errores.

Algunos ejemplos:

```text
404 - Recurso no encontrado
400 - Datos invalidos o duplicados
409 - Conflicto al eliminar un recurso con datos asociados
```

Entre las excepciones personalizadas se encuentran:

- `UsuarioNoEncontradoError`
- `CorreoDuplicadoError`
- `PeliculaNoEncontradaError`
- `SalaNoEncontradaError`
- `FuncionNoEncontradaError`
- `VentaNoEncontradaError`
- `DetalleVentaNoEncontradoError`
- `CodigoBoletoDuplicadoError`

---

# Estructura del proyecto

```text
Cinemax_proyectopy/
|
|-- config/
|   |-- base_datos.py
|   |-- logger.py
|   |-- sistema_config.py
|
|-- dao/
|   |-- usuario_dao.py
|   |-- pelicula_dao.py
|   |-- sala_dao.py
|   |-- funcion_dao.py
|   |-- venta_dao.py
|   |-- detalle_venta_dao.py
|
|-- modelos/
|   |-- usuario.py
|   |-- pelicula.py
|   |-- sala.py
|   |-- funcion.py
|   |-- venta.py
|   |-- detalle_venta.py
|
|-- routers/
|   |-- usuarios.py
|   |-- peliculas.py
|   |-- salas.py
|   |-- funciones.py
|   |-- ventas.py
|   |-- detalles_venta.py
|   |-- registros.py
|
|-- schemas/
|   |-- usuario_schema.py
|   |-- pelicula_schema.py
|   |-- sala_schema.py
|   |-- funcion_schema.py
|   |-- venta_schema.py
|   |-- detalle_venta_schema.py
|
|-- main.py
|-- schema_cine.sql
```

---

## Organizacion de la API

El proyecto separa sus responsabilidades en diferentes capas:

```text
Router
   |
Schema
   |
DAO
   |
Modelo
   |
Base de datos PostgreSQL
```

### Routers

Definen los endpoints de la API y reciben las solicitudes HTTP.

### Schemas

Definen y validan la informacion que recibe y devuelve la API mediante Pydantic.

### DAO

Se encargan de realizar las operaciones de acceso a la base de datos.

### Modelos

Representan las entidades principales del sistema:

- Usuario
- Pelicula
- Sala
- Funcion
- Venta
- Detalle de venta

### Config

Contiene la configuracion de la conexion a la base de datos y el sistema de registros.

---

## CORS

La API permite solicitudes desde los siguientes origenes:

```text
http://localhost:5173
http://localhost:3000
```

---

## Prueba de funcionamiento

Una vez iniciada la API, se puede acceder a:

```text
http://localhost:8000/docs
```

Desde Swagger UI se pueden probar los endpoints de usuarios, peliculas, salas, funciones, ventas, detalles de venta y registros.

---

## Autor

Proyecto academico desarrollado para el sistema de gestion de cine Cinemax.
