import json
from datetime import date, datetime, time

from dao.detalle_venta_dao import (
    CodigoBoletoDuplicadoError,
    DetalleVentaNoEncontradoError,
    ReferenciaDetalleInvalidaError,
)
from dao.funcion_dao import FuncionNoEncontradaError, ReferenciaInvalidaError
from dao.pelicula_dao import PeliculaNoEncontradaError
from dao.sala_dao import SalaNoEncontradaError
from dao.usuario_dao import CorreoDuplicadoError, UsuarioNoEncontradoError
from dao.venta_dao import ReferenciaUsuarioInvalidaError, VentaNoEncontradaError
from modelos.detalle_venta import DetalleVenta
from modelos.funcion import Funcion
from modelos.pelicula import Pelicula
from modelos.sala import Sala
from modelos.usuario import Usuario
from modelos.venta import Venta


def _leer_fecha(texto):
    return date.fromisoformat(texto)


def _leer_hora(texto):
    texto = texto.strip()
    if len(texto) == 5:
        texto = f"{texto}:00"
    return time.fromisoformat(texto)


def _leer_datetime(texto):
    texto = texto.strip()
    if len(texto) == 16:
        texto = f"{texto}:00"
    return datetime.fromisoformat(texto)


def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 45}")
    print(" 1. Agregar usuario")
    print(" 2. Agregar pelicula")
    print(" 3. Agregar sala")
    print(" 4. Agregar funcion")
    print(" 5. Listar usuarios")
    print(" 6. Listar peliculas")
    print(" 7. Listar salas")
    print(" 8. Listar funciones")
    print(" 9. Actualizar usuario")
    print(" 10. Actualizar pelicula")
    print(" 11. Actualizar sala")
    print(" 12. Actualizar funcion")
    print(" 13. Eliminar usuario")
    print(" 14. Eliminar pelicula")
    print(" 15. Eliminar sala")
    print(" 16. Eliminar funcion")
    print(" 17. Ver usuarios en JSON")
    print(" 18. Ver peliculas en JSON")
    print(" 19. Ver salas en JSON")
    print(" 20. Ver funciones en JSON")
    print(" 21. Guardar datos en JSON")
    print(" 22. Show historial de logs")
    print(" 23. Limpiar historial de logs")
    print(" 24. Agregar venta")
    print(" 25. Listar ventas")
    print(" 26. Actualizar venta")
    print(" 27. Eliminar venta")
    print(" 28. Ver ventas en JSON")
    print(" 0. Salir")
    print(f"{'=' * 45}")


def agregar_usuario(udao):
    print("\n--- AGREGAR USUARIO ---")
    nombres_usuario = input(" Nombres : ")
    correo = input(" Correo : ")
    try:
        usuario = udao.insertar(Usuario(nombres_usuario, correo))
        print(f" OK Usuario agregado con ID={usuario.id}")
    except CorreoDuplicadoError as ex:
        print(f" ERROR: {ex}")


def agregar_pelicula(pdao):
    print("\n--- AGREGAR PELICULA ---")
    titulo = input(" Titulo : ")
    genero = input(" Genero : ")
    clasificacion = input(" Clasificacion : ")
    try:
        duracion = int(input(" Duracion en minutos : "))
        pelicula = pdao.insertar(Pelicula(titulo, genero, clasificacion, duracion))
        print(f" OK Pelicula agregada con ID={pelicula.id}")
    except ValueError:
        print(" ERROR: La duracion debe ser un numero entero")


def agregar_sala(sdao):
    print("\n--- AGREGAR SALA ---")
    nombre_sala = input(" Nombre de sala : ")
    try:
        capacidad = int(input(" Capacidad : "))
        sala = sdao.insertar(Sala(nombre_sala, capacidad))
        print(f" OK Sala agregada con ID={sala.id}")
    except ValueError:
        print(" ERROR: La capacidad debe ser un numero entero")


def agregar_funcion(fdao, pdao, sdao):
    print("\n--- AGREGAR FUNCION ---")
    try:
        id_pelicula = int(input(" ID de pelicula : "))
        id_sala = int(input(" ID de sala : "))
        fecha_funcion = _leer_fecha(input(" Fecha (YYYY-MM-DD) : "))
        hora = _leer_hora(input(" Hora (HH:MM o HH:MM:SS) : "))
        precio = float(input(" Precio : "))
        funcion = fdao.insertar(Funcion(id_pelicula, id_sala, fecha_funcion, hora, precio), pdao, sdao)
        print(f" OK Funcion agregada con ID={funcion.id}")
    except ValueError:
        print(" ERROR: Verifica que los numeros, fecha y hora sean validos")
    except ReferenciaInvalidaError as ex:
        print(f" ERROR: {ex}")


def agregar_venta(vdao, udao):
    print("\n--- AGREGAR VENTA ---")
    try:
        id_usuario = int(input(" ID de usuario : "))
        fecha_compra = _leer_datetime(input(" Fecha compra (YYYY-MM-DD HH:MM o HH:MM:SS) : "))
        venta = vdao.insertar(Venta(id_usuario, fecha_compra), udao)
        print(f" OK Venta agregada con ID={venta.id}")
    except ValueError:
        print(" ERROR: Verifica que el ID y la fecha sean validos")
    except ReferenciaUsuarioInvalidaError as ex:
        print(f" ERROR: {ex}")


def agregar_detalle_venta(ddao, vdao, fdao):
    print("\n--- AGREGAR DETALLE DE VENTA ---")
    try:
        id_venta = int(input(" ID de venta : "))
        id_funcion = int(input(" ID de funcion : "))
        asiento = input(" Asiento : ")
        codigo_boleto = input(" Codigo de boleto : ")
        detalle = ddao.insertar(DetalleVenta(id_venta, id_funcion, asiento, codigo_boleto), vdao, fdao)
        print(f" OK Detalle agregado con ID={detalle.id}")
    except ValueError:
        print(" ERROR: Verifica que los IDs sean validos")
    except (ReferenciaDetalleInvalidaError, CodigoBoletoDuplicadoError) as ex:
        print(f" ERROR: {ex}")


def listar_usuarios(udao):
    print("\n--- USUARIOS ---")
    usuarios = udao.obtener_todos()
    if usuarios:
        for usuario in usuarios:
            print(f" {usuario}")
    else:
        print(" (No hay usuarios registrados)")


def listar_peliculas(pdao):
    print("\n--- PELICULAS ---")
    peliculas = pdao.obtener_todos()
    if peliculas:
        for pelicula in peliculas:
            print(f" {pelicula}")
    else:
        print(" (No hay peliculas registradas)")


def listar_salas(sdao):
    print("\n--- SALAS ---")
    salas = sdao.obtener_todos()
    if salas:
        for sala in salas:
            print(f" {sala}")
    else:
        print(" (No hay salas registradas)")


def listar_funciones(fdao):
    print("\n--- FUNCIONES ---")
    funciones = fdao.obtener_todos()
    if funciones:
        for funcion in funciones:
            print(f" {funcion}")
    else:
        print(" (No hay funciones registradas)")


def listar_ventas(vdao):
    print("\n--- VENTAS ---")
    ventas = vdao.obtener_todos()
    if ventas:
        for venta in ventas:
            print(f" {venta}")
    else:
        print(" (No hay ventas registradas)")


def listar_detalles_venta(ddao):
    print("\n--- DETALLES DE VENTA ---")
    detalles = ddao.obtener_todos()
    if detalles:
        for detalle in detalles:
            print(f" {detalle}")
    else:
        print(" (No hay detalles registrados)")


def actualizar_usuario(udao):
    print("\n--- ACTUALIZAR USUARIO ---")
    try:
        usuario_id = int(input(" ID del usuario a actualizar: "))
        nombres_usuario = input(" Nuevos nombres (Enter para no cambiar): ").strip()
        correo = input(" Nuevo correo (Enter para no cambiar): ").strip()
        usuario = udao.actualizar(usuario_id, nombres_usuario or None, correo or None)
        print(f" OK Usuario actualizado: {usuario}")
    except (UsuarioNoEncontradoError, CorreoDuplicadoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def actualizar_pelicula(pdao):
    print("\n--- ACTUALIZAR PELICULA ---")
    try:
        pelicula_id = int(input(" ID de la pelicula a actualizar: "))
        titulo = input(" Nuevo titulo (Enter para no cambiar): ").strip()
        genero = input(" Nuevo genero (Enter para no cambiar): ").strip()
        clasificacion = input(" Nueva clasificacion (Enter para no cambiar): ").strip()
        duracion_str = input(" Nueva duracion (Enter para no cambiar): ").strip()
        duracion = int(duracion_str) if duracion_str else None
        pelicula = pdao.actualizar(pelicula_id, titulo or None, genero or None, clasificacion or None, duracion)
        print(f" OK Pelicula actualizada: {pelicula}")
    except PeliculaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID y la duracion deben ser validos")


def actualizar_sala(sdao):
    print("\n--- ACTUALIZAR SALA ---")
    try:
        sala_id = int(input(" ID de la sala a actualizar: "))
        nombre_sala = input(" Nuevo nombre (Enter para no cambiar): ").strip()
        capacidad_str = input(" Nueva capacidad (Enter para no cambiar): ").strip()
        capacidad = int(capacidad_str) if capacidad_str else None
        sala = sdao.actualizar(sala_id, nombre_sala or None, capacidad)
        print(f" OK Sala actualizada: {sala}")
    except SalaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID y la capacidad deben ser validos")


def actualizar_funcion(fdao, pdao, sdao):
    print("\n--- ACTUALIZAR FUNCION ---")
    try:
        funcion_id = int(input(" ID de la funcion a actualizar: "))
        id_pelicula_str = input(" Nuevo ID de pelicula (Enter para no cambiar): ").strip()
        id_sala_str = input(" Nuevo ID de sala (Enter para no cambiar): ").strip()
        fecha_str = input(" Nueva fecha (YYYY-MM-DD, Enter para no cambiar): ").strip()
        hora_str = input(" Nueva hora (HH:MM o HH:MM:SS, Enter para no cambiar): ").strip()
        precio_str = input(" Nuevo precio (Enter para no cambiar): ").strip()
        funcion = fdao.actualizar(
            funcion_id,
            int(id_pelicula_str) if id_pelicula_str else None,
            int(id_sala_str) if id_sala_str else None,
            _leer_fecha(fecha_str) if fecha_str else None,
            _leer_hora(hora_str) if hora_str else None,
            float(precio_str) if precio_str else None,
            pelicula_dao=pdao,
            sala_dao=sdao,
        )
        print(f" OK Funcion actualizada: {funcion}")
    except (FuncionNoEncontradaError, ReferenciaInvalidaError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: Verifica que los datos sean validos")


def actualizar_venta(vdao, udao):
    print("\n--- ACTUALIZAR VENTA ---")
    try:
        venta_id = int(input(" ID de la venta a actualizar: "))
        id_usuario_str = input(" Nuevo ID de usuario (Enter para no cambiar): ").strip()
        fecha_str = input(" Nueva fecha compra (YYYY-MM-DD HH:MM o HH:MM:SS, Enter para no cambiar): ").strip()
        venta = vdao.actualizar(
            venta_id,
            int(id_usuario_str) if id_usuario_str else None,
            _leer_datetime(fecha_str) if fecha_str else None,
            usuario_dao=udao,
        )
        print(f" OK Venta actualizada: {venta}")
    except (VentaNoEncontradaError, ReferenciaUsuarioInvalidaError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: Verifica que los datos sean validos")


def actualizar_detalle_venta(ddao, vdao, fdao):
    print("\n--- ACTUALIZAR DETALLE DE VENTA ---")
    try:
        detalle_id = int(input(" ID del detalle a actualizar: "))
        id_venta_str = input(" Nuevo ID de venta (Enter para no cambiar): ").strip()
        id_funcion_str = input(" Nuevo ID de funcion (Enter para no cambiar): ").strip()
        asiento = input(" Nuevo asiento (Enter para no cambiar): ").strip()
        codigo_boleto = input(" Nuevo codigo de boleto (Enter para no cambiar): ").strip()
        detalle = ddao.actualizar(
            detalle_id,
            int(id_venta_str) if id_venta_str else None,
            int(id_funcion_str) if id_funcion_str else None,
            asiento or None,
            codigo_boleto or None,
            venta_dao=vdao,
            funcion_dao=fdao,
        )
        print(f" OK Detalle actualizado: {detalle}")
    except (DetalleVentaNoEncontradoError, ReferenciaDetalleInvalidaError, CodigoBoletoDuplicadoError) as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: Verifica que los datos sean validos")


def eliminar_usuario(udao):
    print("\n--- ELIMINAR USUARIO ---")
    try:
        usuario_id = int(input(" ID del usuario a eliminar: "))
        udao.eliminar(usuario_id)
        print(f" OK Usuario ID={usuario_id} eliminado")
    except UsuarioNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_pelicula(pdao):
    print("\n--- ELIMINAR PELICULA ---")
    try:
        pelicula_id = int(input(" ID de la pelicula a eliminar: "))
        pdao.eliminar(pelicula_id)
        print(f" OK Pelicula ID={pelicula_id} eliminada")
    except PeliculaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_sala(sdao):
    print("\n--- ELIMINAR SALA ---")
    try:
        sala_id = int(input(" ID de la sala a eliminar: "))
        sdao.eliminar(sala_id)
        print(f" OK Sala ID={sala_id} eliminada")
    except SalaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_funcion(fdao):
    print("\n--- ELIMINAR FUNCION ---")
    try:
        funcion_id = int(input(" ID de la funcion a eliminar: "))
        fdao.eliminar(funcion_id)
        print(f" OK Funcion ID={funcion_id} eliminada")
    except FuncionNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_venta(vdao):
    print("\n--- ELIMINAR VENTA ---")
    try:
        venta_id = int(input(" ID de la venta a eliminar: "))
        vdao.eliminar(venta_id)
        print(f" OK Venta ID={venta_id} eliminada")
    except VentaNoEncontradaError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def eliminar_detalle_venta(ddao):
    print("\n--- ELIMINAR DETALLE DE VENTA ---")
    try:
        detalle_id = int(input(" ID del detalle a eliminar: "))
        ddao.eliminar(detalle_id)
        print(f" OK Detalle ID={detalle_id} eliminado")
    except DetalleVentaNoEncontradoError as ex:
        print(f" ERROR: {ex}")
    except ValueError:
        print(" ERROR: El ID debe ser un numero entero")


def ver_usuarios_json(udao):
    print("\n--- USUARIOS EN JSON ---")
    usuarios = udao.obtener_todos()
    if usuarios:
        print(json.dumps([usuario.to_dict() for usuario in usuarios], indent=4, ensure_ascii=False))
    else:
        print(" (No hay usuarios registrados)")


def ver_peliculas_json(pdao):
    print("\n--- PELICULAS EN JSON ---")
    peliculas = pdao.obtener_todos()
    if peliculas:
        print(json.dumps([pelicula.to_dict() for pelicula in peliculas], indent=4, ensure_ascii=False))
    else:
        print(" (No hay peliculas registradas)")


def ver_salas_json(sdao):
    print("\n--- SALAS EN JSON ---")
    salas = sdao.obtener_todos()
    if salas:
        print(json.dumps([sala.to_dict() for sala in salas], indent=4, ensure_ascii=False))
    else:
        print(" (No hay salas registradas)")


def ver_funciones_json(fdao):
    print("\n--- FUNCIONES EN JSON ---")
    funciones = fdao.obtener_todos()
    if funciones:
        print(json.dumps([funcion.to_dict() for funcion in funciones], indent=4, ensure_ascii=False))
    else:
        print(" (No hay funciones registradas)")


def ver_ventas_json(vdao):
    print("\n--- VENTAS EN JSON ---")
    ventas = vdao.obtener_todos()
    if ventas:
        print(json.dumps([venta.to_dict() for venta in ventas], indent=4, ensure_ascii=False))
    else:
        print(" (No hay ventas registradas)")


def ver_detalles_json(ddao):
    print("\n--- DETALLES DE VENTA EN JSON ---")
    detalles = ddao.obtener_todos()
    if detalles:
        print(json.dumps([detalle.to_dict() for detalle in detalles], indent=4, ensure_ascii=False))
    else:
        print(" (No hay detalles registrados)")
