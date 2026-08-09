# Proyecto CineMax - Guia rapida

Este proyecto sigue la misma idea del ejemplo base:

1. Los objetos viven en memoria dentro de cada DAO.
2. Al iniciar, `config/persistencia.py` carga datos desde JSON.
3. Al salir, el programa guarda todos los datos otra vez en JSON.
4. Cada modelo tiene `to_dict()` y `from_dict()` para serializar y reconstruir objetos.
5. `Logger` y `SistemaConfig` usan el patron singleton.

## Archivos principales

- `main.py`: arranque y ciclo del menu.
- `vistas/menu.py`: opciones de consola.
- `dao/`: insercion, busqueda, actualizacion y eliminacion.
- `modelos/`: clases de entidad.
- `config/persistencia.py`: guardado y carga JSON.

## Persistencia

Los archivos JSON se guardan en la raiz del proyecto:

- `datos_usuarios.json`
- `datos_peliculas.json`
- `datos_salas.json`
- `datos_funciones.json`
- `datos_ventas.json`
- `datos_detalles_venta.json`
