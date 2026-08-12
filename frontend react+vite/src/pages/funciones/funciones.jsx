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
import "./funciones.css";

function Funciones() {
  const [funciones, setFunciones] = useState([]);
  const [peliculas, setPeliculas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [idPelicula, setIdPelicula] = useState("");
  const [idSala, setIdSala] = useState("");
  const [fechaFuncion, setFechaFuncion] = useState("");
  const [hora, setHora] = useState("");
  const [precio, setPrecio] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [funcionEliminar, setFuncionEliminar] = useState(null);

  const cargarDatos = async () => {
    try {
      const [respuestaFunciones, respuestaPeliculas, respuestaSalas] = await Promise.all([
        api.get("/funciones/"),
        api.get("/peliculas/"),
        api.get("/salas/"),
      ]);

      setFunciones(respuestaFunciones.data);
      setPeliculas(respuestaPeliculas.data);
      setSalas(respuestaSalas.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar las funciones",
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

  const salasPorId = useMemo(
    () => new Map(salas.map((sala) => [sala.id, sala])),
    [salas],
  );

  const salasRelacionadas = useMemo(() => {
    if (!idPelicula) {
      return [];
    }

    return salas.filter((sala) => sala.id_pelicula === Number(idPelicula));
  }, [idPelicula, salas]);

  useEffect(() => {
    if (!idPelicula) {
      setIdSala("");
      return;
    }

    const salaSeleccionadaExiste = salasRelacionadas.some(
      (sala) => String(sala.id) === idSala,
    );

    if (!salaSeleccionadaExiste) {
      setIdSala(salasRelacionadas[0] ? String(salasRelacionadas[0].id) : "");
    }
  }, [idPelicula, idSala, salasRelacionadas]);

  const limpiarFormulario = () => {
    setIdEditar(null);
    setIdPelicula("");
    setIdSala("");
    setFechaFuncion("");
    setHora("");
    setPrecio("");
  };

  const validarFormulario = () => {
    const precioNumerico = Number(precio);

    if (!idPelicula || !idSala || fechaFuncion === "" || hora === "" || precio === "") {
      setMensaje(mensajeInfo("Campos incompletos", "Complete pelicula, sala, fecha, hora y precio."));
      return false;
    }

    if (salasRelacionadas.length === 0) {
      setMensaje(mensajeInfo("Sala requerida", "Registre una sala asociada a la pelicula."));
      return false;
    }

    if (Number.isNaN(precioNumerico) || precioNumerico <= 0) {
      setMensaje(mensajeInfo("Precio invalido", "El precio debe ser mayor que cero."));
      return false;
    }

    return true;
  };

  const datosFuncion = () => ({
    id_pelicula: Number(idPelicula),
    id_sala: Number(idSala),
    fecha_funcion: fechaFuncion,
    hora,
    precio: Number(precio),
  });

  const guardarFuncion = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.post("/funciones/", datosFuncion());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Funcion registrada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "La funcion no pudo registrarse."),
        ),
      );
    }
  };

  const editarFuncion = (funcion) => {
    setIdEditar(funcion.id);
    setIdPelicula(String(funcion.id_pelicula));
    setIdSala(String(funcion.id_sala));
    setFechaFuncion(funcion.fecha_funcion);
    setHora(String(funcion.hora).slice(0, 5));
    setPrecio(String(funcion.precio));
    setMensaje(null);
  };

  const actualizarFuncion = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.put(`/funciones/${idEditar}`, datosFuncion());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Funcion actualizada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "La funcion no pudo actualizarse."),
        ),
      );
    }
  };

  const eliminarFuncion = async () => {
    if (!funcionEliminar) {
      return;
    }

    try {
      await api.delete(`/funciones/${funcionEliminar.id}`);
      await cargarDatos();
      setFuncionEliminar(null);
      setMensaje(mensajeExito("Funcion eliminada", "El registro fue eliminado correctamente."));
    } catch (error) {
      setFuncionEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "La funcion tiene boletos relacionados."),
        ),
      );
    }
  };

  const funcionesFiltradas = funciones.filter((funcion) => {
    const pelicula = peliculasPorId.get(funcion.id_pelicula);
    const sala = salasPorId.get(funcion.id_sala);
    const texto = busqueda.toLowerCase();
    const resumen = [
      pelicula?.titulo,
      sala?.nombre_sala,
      funcion.fecha_funcion,
      funcion.hora,
      funcion.precio,
    ]
      .join(" ")
      .toLowerCase();

    return resumen.includes(texto);
  });

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Funciones" />

        <div className="page-content funciones-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-calendar-plus-fill"} me-2`}></i>
                    {idEditar ? "Editar Funcion" : "Registrar Funcion"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="peliculaFuncion">
                      Pelicula
                    </label>
                    <select
                      id="peliculaFuncion"
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
                    <label className="form-label" htmlFor="salaFuncion">
                      Sala
                    </label>
                    <select
                      id="salaFuncion"
                      className="form-select"
                      value={idSala}
                      onChange={(event) => setIdSala(event.target.value)}
                      disabled={!idPelicula || salasRelacionadas.length === 0}
                    >
                      <option value="">
                        {!idPelicula
                          ? "Seleccione una pelicula primero"
                          : "Seleccionar sala"}
                      </option>
                      {salasRelacionadas.map((sala) => (
                        <option key={sala.id} value={sala.id}>
                          {sala.nombre_sala} ({sala.asientos_disponibles ?? sala.capacidad}/{sala.capacidad} asientos)
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label" htmlFor="fechaFuncion">
                        Fecha
                      </label>
                      <input
                        id="fechaFuncion"
                        type="date"
                        className="form-control"
                        value={fechaFuncion}
                        onChange={(event) => setFechaFuncion(event.target.value)}
                      />
                    </div>

                    <div className="col-md-6 mb-3">
                      <label className="form-label" htmlFor="horaFuncion">
                        Hora
                      </label>
                      <input
                        id="horaFuncion"
                        type="time"
                        className="form-control"
                        value={hora}
                        onChange={(event) => setHora(event.target.value)}
                      />
                    </div>
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="precioFuncion">
                      Precio
                    </label>
                    <input
                      id="precioFuncion"
                      type="number"
                      min="0.01"
                      step="0.01"
                      className="form-control"
                      value={precio}
                      onChange={(event) => setPrecio(event.target.value)}
                      placeholder="Precio de entrada"
                    />
                  </div>

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarFuncion : guardarFuncion}
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
                    <i className="bi bi-calendar-event-fill me-2"></i>
                    Funciones registradas
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
                        placeholder="Buscar por pelicula, sala, fecha o precio..."
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
                          <th>Fecha</th>
                          <th>Hora</th>
                          <th>Precio</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {funcionesFiltradas.length === 0 ? (
                          <tr>
                            <td colSpan="7" className="empty-row">
                              {funciones.length === 0
                                ? "No existen funciones registradas"
                                : "No se encontraron funciones con esa busqueda"}
                            </td>
                          </tr>
                        ) : (
                          funcionesFiltradas.map((funcion) => (
                            <tr key={funcion.id}>
                              <td>{funcion.id}</td>
                              <td>{peliculasPorId.get(funcion.id_pelicula)?.titulo ?? `Pelicula ${funcion.id_pelicula}`}</td>
                              <td>{salasPorId.get(funcion.id_sala)?.nombre_sala ?? `Sala ${funcion.id_sala}`}</td>
                              <td>{funcion.fecha_funcion}</td>
                              <td>{String(funcion.hora).slice(0, 5)}</td>
                              <td>S/. {Number(funcion.precio).toFixed(2)}</td>
                              <td>
                                <div className="acciones-tabla">
                                  <button
                                    type="button"
                                    className="btn btn-warning btn-sm"
                                    onClick={() => editarFuncion(funcion)}
                                    title="Editar funcion"
                                  >
                                    <i className="bi bi-pencil-square"></i>
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-danger btn-sm"
                                    onClick={() => setFuncionEliminar(funcion)}
                                    title="Eliminar funcion"
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
        abierta={Boolean(funcionEliminar)}
        titulo="Eliminar funcion"
        mensaje="Se eliminara la funcion seleccionada del sistema."
        textoConfirmar="Eliminar"
        onCancelar={() => setFuncionEliminar(null)}
        onConfirmar={eliminarFuncion}
      />
    </>
  );
}

export default Funciones;
