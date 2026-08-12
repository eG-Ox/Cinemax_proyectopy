import { useEffect, useMemo, useState } from "react";

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
import "./salas.css";

function Salas() {
  const [salas, setSalas] = useState([]);
  const [peliculas, setPeliculas] = useState([]);
  const [idPelicula, setIdPelicula] = useState("");
  const [nombreSala, setNombreSala] = useState("");
  const [capacidad, setCapacidad] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [salaEliminar, setSalaEliminar] = useState(null);

  const cargarDatos = async () => {
    try {
      const [respuestaSalas, respuestaPeliculas] = await Promise.all([
        api.get("/salas/"),
        api.get("/peliculas/"),
      ]);

      setSalas(respuestaSalas.data);
      setPeliculas(respuestaPeliculas.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar las salas",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const peliculasPorId = useMemo(
    () => new Map(peliculas.map((pelicula) => [pelicula.id, pelicula])),
    [peliculas],
  );

  const limpiarFormulario = () => {
    setIdEditar(null);
    setIdPelicula("");
    setNombreSala("");
    setCapacidad("");
  };

  const validarFormulario = () => {
    const capacidadNumerica = Number(capacidad);

    if (!idPelicula || nombreSala.trim() === "" || capacidad === "") {
      setMensaje(mensajeInfo("Campos incompletos", "Complete pelicula, nombre y capacidad."));
      return false;
    }

    if (!Number.isInteger(capacidadNumerica) || capacidadNumerica <= 0) {
      setMensaje(mensajeInfo("Capacidad invalida", "La capacidad debe ser un entero mayor que cero."));
      return false;
    }

    return true;
  };

  const datosSala = () => ({
    id_pelicula: Number(idPelicula),
    nombre_sala: nombreSala.trim(),
    capacidad: Number(capacidad),
  });

  const guardarSala = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.post("/salas/", datosSala());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Sala registrada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "La sala no pudo registrarse."),
        ),
      );
    }
  };

  const editarSala = (sala) => {
    setIdEditar(sala.id);
    setIdPelicula(sala.id_pelicula ? String(sala.id_pelicula) : "");
    setNombreSala(sala.nombre_sala);
    setCapacidad(String(sala.capacidad));
    setMensaje(null);
  };

  const actualizarSala = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.put(`/salas/${idEditar}`, datosSala());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Sala actualizada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "La sala no pudo actualizarse."),
        ),
      );
    }
  };

  const eliminarSala = async () => {
    if (!salaEliminar) {
      return;
    }

    try {
      await api.delete(`/salas/${salaEliminar.id}`);
      await cargarDatos();
      setSalaEliminar(null);
      setMensaje(mensajeExito("Sala eliminada", "El registro fue eliminado correctamente."));
    } catch (error) {
      setSalaEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "La sala tiene funciones relacionadas."),
        ),
      );
    }
  };

  const salasFiltradas = salas.filter((sala) => {
    const pelicula = peliculasPorId.get(sala.id_pelicula);
    const texto = busqueda.toLowerCase();
    return (
      pelicula?.titulo.toLowerCase().includes(texto) ||
      sala.nombre_sala.toLowerCase().includes(texto) ||
      String(sala.capacidad).includes(texto) ||
      String(sala.asientos_disponibles ?? sala.capacidad).includes(texto)
    );
  });

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Salas" />

        <div className="page-content salas-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-grid-3x3-gap-fill"} me-2`}></i>
                    {idEditar ? "Editar Sala" : "Registrar Sala"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="peliculaSala">
                      Pelicula
                    </label>
                    <select
                      id="peliculaSala"
                      className="form-select"
                      value={idPelicula}
                      onChange={(event) => setIdPelicula(event.target.value)}
                    >
                      <option value="">Seleccionar pelicula</option>
                      {peliculas.map((pelicula) => (
                        <option key={pelicula.id} value={pelicula.id}>
                          {pelicula.titulo}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="nombreSala">
                      Nombre de sala
                    </label>
                    <input
                      id="nombreSala"
                      className="form-control"
                      value={nombreSala}
                      onChange={(event) => setNombreSala(event.target.value)}
                      placeholder="Sala 1"
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="capacidadSala">
                      Capacidad
                    </label>
                    <input
                      id="capacidadSala"
                      type="number"
                      min="1"
                      className="form-control"
                      value={capacidad}
                      onChange={(event) => setCapacidad(event.target.value)}
                      placeholder="Cantidad de asientos"
                    />
                  </div>

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarSala : guardarSala}
                  >
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-save-fill"} me-2`}></i>
                    {idEditar ? "Actualizar" : "Guardar"}
                  </button>

                  <button
                    type="button"
                    className="btn btn-secondary ms-2"
                    onClick={limpiarFormulario}
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
                    <i className="bi bi-building-fill me-2"></i>
                    Salas registradas
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
                        placeholder="Buscar por pelicula, nombre o capacidad..."
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
                          <th>Pelicula</th>
                          <th>Sala</th>
                          <th>Capacidad</th>
                          <th>Disponibles</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {salasFiltradas.length === 0 ? (
                          <tr>
                            <td colSpan="6" className="empty-row">
                              {salas.length === 0
                                ? "No existen salas registradas"
                                : "No se encontraron salas con esa busqueda"}
                            </td>
                          </tr>
                        ) : (
                          salasFiltradas.map((sala) => (
                            <tr key={sala.id}>
                              <td>{sala.id}</td>
                              <td>
                                {peliculasPorId.get(sala.id_pelicula)?.titulo ??
                                  "Sin pelicula"}
                              </td>
                              <td>{sala.nombre_sala}</td>
                              <td>{sala.capacidad} asientos</td>
                              <td>{sala.asientos_disponibles ?? sala.capacidad} asientos</td>
                              <td>
                                <div className="acciones-tabla">
                                  <button
                                    type="button"
                                    className="btn btn-warning btn-sm"
                                    onClick={() => editarSala(sala)}
                                    title="Editar sala"
                                  >
                                    <i className="bi bi-pencil-square"></i>
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-danger btn-sm"
                                    onClick={() => setSalaEliminar(sala)}
                                    title="Eliminar sala"
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
        abierta={Boolean(salaEliminar)}
        titulo="Eliminar sala"
        mensaje={`Se eliminara ${salaEliminar?.nombre_sala ?? "esta sala"} del sistema.`}
        textoConfirmar="Eliminar"
        onCancelar={() => setSalaEliminar(null)}
        onConfirmar={eliminarSala}
      />
    </>
  );
}

export default Salas;
