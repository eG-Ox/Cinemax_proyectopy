from fastapi import APIRouter
from config.logger import Logger

router = APIRouter(prefix="/registros", tags=["Registros"])
logger = Logger()


@router.get("/")
def obtener_registros():
    registros = []

    for log in logger._logs:
        mensaje = log["msg"]
        modulo = "Sistema"
        accion = "Informacion"
        informacion = mensaje

        if mensaje.startswith("Usuario agregado:"):
            modulo = "Usuarios"
            accion = "Registrar"
            informacion = mensaje.replace("Usuario agregado:", "").strip()
        elif mensaje.startswith("Usuario actualizado:"):
            modulo = "Usuarios"
            accion = "Actualizar"
            informacion = mensaje.replace("Usuario actualizado:", "").strip()
        elif mensaje.startswith("Usuario eliminado:"):
            modulo = "Usuarios"
            accion = "Eliminar"
            informacion = mensaje.replace("Usuario eliminado:", "").strip()
        elif mensaje.startswith("Pelicula agregada:"):
            modulo = "Peliculas"
            accion = "Registrar"
            informacion = mensaje.replace("Pelicula agregada:", "").strip()
        elif mensaje.startswith("Pelicula actualizada:"):
            modulo = "Peliculas"
            accion = "Actualizar"
            informacion = mensaje.replace("Pelicula actualizada:", "").strip()
        elif mensaje.startswith("Pelicula eliminada:"):
            modulo = "Peliculas"
            accion = "Eliminar"
            informacion = mensaje.replace("Pelicula eliminada:", "").strip()
        elif mensaje.startswith("Sala agregada:"):
            modulo = "Salas"
            accion = "Registrar"
            informacion = mensaje.replace("Sala agregada:", "").strip()
        elif mensaje.startswith("Sala actualizada:"):
            modulo = "Salas"
            accion = "Actualizar"
            informacion = mensaje.replace("Sala actualizada:", "").strip()
        elif mensaje.startswith("Sala eliminada:"):
            modulo = "Salas"
            accion = "Eliminar"
            informacion = mensaje.replace("Sala eliminada:", "").strip()
        elif mensaje.startswith("Funcion agregada:"):
            modulo = "Funciones"
            accion = "Registrar"
            informacion = mensaje.replace("Funcion agregada:", "").strip()
        elif mensaje.startswith("Funcion actualizada:"):
            modulo = "Funciones"
            accion = "Actualizar"
            informacion = mensaje.replace("Funcion actualizada:", "").strip()
        elif mensaje.startswith("Funcion eliminada:"):
            modulo = "Funciones"
            accion = "Eliminar"
            informacion = mensaje.replace("Funcion eliminada:", "").strip()
        elif mensaje.startswith("Venta agregada:"):
            modulo = "Ventas"
            accion = "Registrar"
            informacion = mensaje.replace("Venta agregada:", "").strip()
        elif mensaje.startswith("Venta actualizada:"):
            modulo = "Ventas"
            accion = "Actualizar"
            informacion = mensaje.replace("Venta actualizada:", "").strip()
        elif mensaje.startswith("Venta eliminada:"):
            modulo = "Ventas"
            accion = "Eliminar"
            informacion = mensaje.replace("Venta eliminada:", "").strip()
        elif mensaje.startswith("Detalle de venta agregado:"):
            modulo = "Detalles de venta"
            accion = "Registrar"
            informacion = mensaje.replace("Detalle de venta agregado:", "").strip()
        elif mensaje.startswith("Detalle de venta actualizado:"):
            modulo = "Detalles de venta"
            accion = "Actualizar"
            informacion = mensaje.replace("Detalle de venta actualizado:", "").strip()
        elif mensaje.startswith("Detalle de venta eliminado:"):
            modulo = "Detalles de venta"
            accion = "Eliminar"
            informacion = mensaje.replace("Detalle de venta eliminado:", "").strip()

        registros.append({
            "hora": log["hora"],
            "nivel": log["nivel"],
            "modulo": modulo,
            "accion": accion,
            "informacion": informacion,
        })

    return registros


@router.delete("/")
def eliminar_historial():
    logger.limpiar()
    return {"mensaje": "Historial eliminado correctamente"}
