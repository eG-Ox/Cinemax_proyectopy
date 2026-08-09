# CineMax

Proyecto de consola en Python para gestionar un cine con datos en memoria y persistencia JSON.

## Ejecutar

```powershell
python main.py
```

## Modulos principales

- `modelos/`: entidades del sistema.
- `dao/`: operaciones CRUD y validaciones.
- `config/`: configuracion, logger y persistencia.
- `vistas/menu.py`: interfaz de consola.
- `schema_cine.sql`: estructura relacional equivalente.

## Entidades

- Usuarios
- Peliculas
- Salas
- Funciones
- Ventas
- Detalles de venta

Los datos se guardan en archivos `datos_*.json` al salir o al usar la opcion de guardado.
