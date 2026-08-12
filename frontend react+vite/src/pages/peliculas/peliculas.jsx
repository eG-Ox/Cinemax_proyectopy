import { useEffect, useRef, useState } from "react";

import api from "../../api/axios";
import Confirmacion from "../../components/confirmacion/confirmacion";
import Header from "../../components/header/header";
import Mensaje from "../../components/mensaje/mensaje";
import Menu from "../../components/menu/menu";
import {
  mensajeError,
  mensajeExito,
  mensajeInfo,
  obtenerMensajeError,
} from "../../utils/mensajes";
import "./peliculas.css";

const clasificaciones = ["G", "PG", "PG-13", "R", "NC-17", "+14", "+18"];

function Peliculas() {
  const [peliculas, setPeliculas] = useState([]);
  const [titulo, setTitulo] = useState("");
  const [genero, setGenero] = useState("");
  const [clasificacion, setClasificacion] = useState("PG-13");
  const [duracion, setDuracion] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [peliculaEliminar, setPeliculaEliminar] = useState(null);
  const [guardando, setGuardando] = useState(false);
  const guardandoRef = useRef(false);

  const cargarPeliculas = async () => {
    try {
      const respuesta = await api.get("/peliculas/");
      setPeliculas(respuesta.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar las peliculas",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarPeliculas();
  }, []);

  const limpiarFormulario = () => {
    setIdEditar(null);
    setTitulo("");
    setGenero("");
    setClasificacion("PG-13");
    setDuracion("");
  };

  const validarFormulario = () => {
    const duracionNumerica = Number(duracion);

    if (titulo.trim() === "" || genero.trim() === "" || duracion === "") {
      setMensaje(mensajeInfo("Campos incompletos", "Complete todos los datos de la pelicula."));
      return false;
    }

    if (!Number.isInteger(duracionNumerica) || duracionNumerica <= 0) {
      setMensaje(mensajeInfo("Duracion invalida", "La duracion debe ser un entero mayor que cero."));
      return false;
    }

    return true;
  };

  const datosPelicula = () => ({
    titulo: titulo.trim(),
    genero: genero.trim(),
    clasificacion,
    duracion: Number(duracion),
  });

  const guardarPelicula = async () => {
    if (guardandoRef.current || !validarFormulario()) {
      return;
    }

    guardandoRef.current = true;
    setGuardando(true);

    try {
      await api.post("/peliculas/", datosPelicula());
      await cargarPeliculas();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Pelicula registrada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "La pelicula no pudo registrarse."),
        ),
      );
    } finally {
      guardandoRef.current = false;
      setGuardando(false);
    }
  };

  const editarPelicula = (pelicula) => {
    setIdEditar(pelicula.id);
    setTitulo(pelicula.titulo);
    setGenero(pelicula.genero);
    setClasificacion(pelicula.clasificacion);
    setDuracion(String(pelicula.duracion));
    setMensaje(null);
  };

  const actualizarPelicula = async () => {
    if (guardandoRef.current || !validarFormulario()) {
      return;
    }

    guardandoRef.current = true;
    setGuardando(true);

    try {
      await api.put(`/peliculas/${idEditar}`, datosPelicula());
      await cargarPeliculas();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Pelicula actualizada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "La pelicula no pudo actualizarse."),
        ),
      );
    } finally {
      guardandoRef.current = false;
      setGuardando(false);
    }
  };

  const eliminarPelicula = async () => {
    if (!peliculaEliminar) {
      return;
    }

    try {
      await api.delete(`/peliculas/${peliculaEliminar.id}`);
      await cargarPeliculas();
      setPeliculaEliminar(null);
      setMensaje(mensajeExito("Pelicula eliminada", "El registro fue eliminado correctamente."));
    } catch (error) {
      setPeliculaEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "La pelicula tiene funciones relacionadas."),
        ),
      );
    }
  };

  const peliculasFiltradas = peliculas.filter((pelicula) => {
    const texto = busqueda.toLowerCase();
    return (
      pelicula.titulo.toLowerCase().includes(texto) ||
      pelicula.genero.toLowerCase().includes(texto) ||
      pelicula.clasificacion.toLowerCase().includes(texto)
    );
  });

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Peliculas" />

        <div className="page-content peliculas-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-film"} me-2`}></i>
                    {idEditar ? "Editar Pelicula" : "Registrar Pelicula"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="tituloPelicula">
                      Titulo
                    </label>
                    <input
                      id="tituloPelicula"
                      className="form-control"
                      value={titulo}
                      onChange={(event) => setTitulo(event.target.value)}
                      placeholder="Titulo de la pelicula"
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="generoPelicula">
                      Genero
                    </label>
                    <input
                      id="generoPelicula"
                      className="form-control"
                      value={genero}
                      onChange={(event) => setGenero(event.target.value)}
                      placeholder="Accion, drama, comedia..."
                    />
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label" htmlFor="clasificacionPelicula">
                        Clasificacion
                      </label>
                      <select
                        id="clasificacionPelicula"
                        className="form-select"
                        value={clasificacion}
                        onChange={(event) => setClasificacion(event.target.value)}
                      >
                        {clasificaciones.map((item) => (
                          <option key={item} value={item}>
                            {item}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label" htmlFor="duracionPelicula">
                        Duracion
                      </label>
                      <input
                        id="duracionPelicula"
                        type="number"
                        min="1"
                        className="form-control"
                        value={duracion}
                        onChange={(event) => setDuracion(event.target.value)}
                        placeholder="Minutos"
                      />
                    </div>
                  </div>

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarPelicula : guardarPelicula}
                    disabled={guardando}
                  >
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-save-fill"} me-2`}></i>
                    {guardando ? "Guardando..." : idEditar ? "Actualizar" : "Guardar"}
                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary ms-2"
                    onClick={limpiarFormulario}
                    disabled={guardando}
                  >
                    <i className="bi bi-eraser-fill me-2"></i>
                    Limpiar
                  </button>
                </div>
              </div>
            </div>

            <div className="col-lg-8">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className="bi bi-collection-play-fill me-2"></i>
                    Peliculas registradas
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="bi bi-search"></i>
                      </span>
                      <input
                        className="form-control"
                        placeholder="Buscar por titulo, genero o clasificacion..."
                        value={busqueda}
                        onChange={(event) => setBusqueda(event.target.value)}
                      />
                    </div>
                  </div>

                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Titulo</th>
                          <th>Genero</th>
                          <th>Clasificacion</th>
                          <th>Duracion</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {peliculasFiltradas.length === 0 ? (
                          <tr>
                            <td colSpan="6" className="empty-row">
                              {peliculas.length === 0
                                ? "No existen peliculas registradas"
                                : "No se encontraron peliculas con esa busqueda"}
                            </td>
                          </tr>
                        ) : (
                          peliculasFiltradas.map((pelicula) => (
                            <tr key={pelicula.id}>
                              <td>{pelicula.id}</td>
                              <td>{pelicula.titulo}</td>
                              <td>{pelicula.genero}</td>
                              <td>
                                <span className="badge badge-soft">{pelicula.clasificacion}</span>
                              </td>
                              <td>{pelicula.duracion} min</td>
                              <td>
                                <div className="acciones-tabla">
                                  <button
                                    type="button"
                                    className="btn btn-warning btn-sm"
                                    onClick={() => editarPelicula(pelicula)}
                                    title="Editar pelicula"
                                  >
                                    <i className="bi bi-pencil-square"></i>
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-danger btn-sm"
                                    onClick={() => setPeliculaEliminar(pelicula)}
                                    title="Eliminar pelicula"
                                  >
                                    <i className="bi bi-trash-fill"></i>
                                  </button>
                                </div>
                              </td>
                            </tr>
                          ))
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Confirmacion
        abierta={Boolean(peliculaEliminar)}
        titulo="Eliminar pelicula"
        mensaje={`Se eliminara ${peliculaEliminar?.titulo ?? "esta pelicula"} del catalogo.`}
        textoConfirmar="Eliminar"
        onCancelar={() => setPeliculaEliminar(null)}
        onConfirmar={eliminarPelicula}
      />
    </>
  );
}

export default Peliculas;
