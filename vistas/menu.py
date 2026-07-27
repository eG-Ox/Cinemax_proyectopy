import json

from dao.pelicula_dao import PeliculaNoEncontradaError
from dao.sala_dao import SalaNoEncontradaError
from dao.usuario_dao import CorreoDuplicadoError, UsuarioNoEncontradoError
from modelos.pelicula import Pelicula
from modelos.sala import Sala
from modelos.usuario import Usuario


def mostrar_menu(cfg):
    print(f"\n{'=' * 45}")
    print(f" {cfg.nombre} v{cfg.version}")
    print(f" {cfg.empresa}")
    print(f"{'=' * 45}")
    print(" 1. Agregar usuario")
    print(" 2. Agregar pelicula")
    print(" 3. Agregar sala")
    print(" 4. Listar usuarios")
    print(" 5. Listar peliculas")
    print(" 6. Listar salas")
    print(" 7. Actualizar usuario")
    print(" 8. Actualizar pelicula")
    print(" 9. Actualizar sala")
    print(" 10. Eliminar usuario")
    print(" 11. Eliminar pelicula")
    print(" 12. Eliminar sala")
    print(" 13. Ver usuarios en JSON")
    print(" 14. Ver peliculas en JSON")
    print(" 15. Ver salas en JSON")
    print(" 16. Guardar datos en JSON")
    print(" 17. Show historial de logs")
    print(" 18. Limpiar historial de logs")
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
