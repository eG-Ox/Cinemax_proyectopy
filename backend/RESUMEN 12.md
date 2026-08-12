# Semana 12 — Persistencia con JSON

## Objetivo
Agregar persistencia de datos usando archivos JSON, de modo que la información sobreviva al cierre del programa.

## Qué cambió respecto a semana-11

| Archivo | Cambio |
|---|---|
| `config/persistencia.py` | **Nuevo** — funciones para guardar y cargar JSON |
| `modelos/cliente.py` | Se agregan `to_dict()` y `from_dict()` |
| `modelos/producto.py` | Se agregan `to_dict()` y `from_dict()` |
| `main.py` | Carga datos al iniciar, guarda al salir |
| `vistas/menu.py` | Opciones 9-13 nuevas |
| `dao/` | Sin cambios |

## Cómo ejecutar

> Requiere Python 3.10 o superior

```bash
cd semana-12
python main.py
```

Al ejecutar por primera vez verás:
```
AVISO: No existe 'datos_clientes.json', se empieza desde cero
AVISO: No existe 'datos_productos.json', se empieza desde cero
```
Eso es normal. Agrega algunos clientes y productos, luego cierra con `0`. La próxima vez que ejecutes el programa, los datos estarán ahí.

---

## Archivos generados

```
semana-12/
├── datos_clientes.json    ← se crea automáticamente al guardar
└── datos_productos.json   ← se crea automáticamente al guardar
```

Ejemplo de `datos_clientes.json`:
```json
[
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "ruc": "20123456789",
        "email": "juan@empresa.com",
        "telefono": "987654321"
    }
]
```

---

## Archivos clave explicados

### `modelos/cliente.py` — Serialización
Se agregan dos métodos nuevos:

```python
def to_dict(self):
    return {
        "id": self.id, "nombre": self.nombre,
        "ruc": self.ruc, "email": self.email, "telefono": self.telefono
    }

@classmethod
def from_dict(cls, datos):
    c = cls(datos["nombre"], datos["ruc"], datos["email"], datos["telefono"])
    c.id = datos["id"]
    return c
```

- `to_dict()` convierte el objeto a un diccionario que Python puede escribir en JSON
- `from_dict()` es un **classmethod** que reconstruye el objeto desde un diccionario leído del JSON

---

### `config/persistencia.py` — Guardar y cargar
```python
def guardar_clientes(cdao):
    datos = [c.to_dict() for c in cdao.obtener_todos()]  # lista de dicts
    with open("datos_clientes.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def cargar_clientes(cdao):
    with open("datos_clientes.json", "r", encoding="utf-8") as f:
        datos = json.load(f)
    for d in datos:
        cliente = Cliente.from_dict(d)
        cdao._ClienteDAO__bd.append(cliente)   # acceso al atributo privado
        if cliente.id >= cdao._ClienteDAO__cid:
            cdao._ClienteDAO__cid = cliente.id + 1
```

**Nota sobre `_ClienteDAO__bd`:** En Python, `self.__bd` dentro de una clase se convierte internamente en `_ClienteDAO__bd`. Esto se llama **name mangling** y es una forma de proteger atributos privados. Aquí se accede directamente para cargar los datos sin pasar por `insertar()` (que validaría RUC duplicado y generaría un ID nuevo).

---

### `main.py` — Carga automática al iniciar
```python
cdao = ClienteDAO()
pdao = ProductoDAO()

cargar_clientes(cdao)   # carga desde JSON antes del menú
cargar_productos(pdao)

# ...al salir:
case "0":
    guardar_clientes(cdao)   # guarda automáticamente
    guardar_productos(pdao)
    break
```

---

## Limitación de esta versión
Los datos se guardan en archivos del mismo directorio. Si borras `datos_clientes.json`, pierdes todo. Tampoco puedes tener dos instancias del programa corriendo a la vez sin conflicto. Eso se resuelve en la siguiente semana con una base de datos real.

---

## Ejercicio propuesto
1. Agrega un método `buscar_por_nombre(nombre)` en `ClienteDAO` que busque por nombre (sin importar mayúsculas/minúsculas)
2. Agrega la opción 14 en el menú que use ese método
3. Verifica que al guardar y volver a cargar, el nuevo campo siga funcionando
