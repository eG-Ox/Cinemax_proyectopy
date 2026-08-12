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
import "./detalles.css";

function DetallesVenta() {
  const [detalles, setDetalles] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [funciones, setFunciones] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [peliculas, setPeliculas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [idVenta, setIdVenta] = useState("");
  const [idFuncion, setIdFuncion] = useState("");
  const [asiento, setAsiento] = useState("");
  const [codigoBoleto, setCodigoBoleto] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [filtroVenta, setFiltroVenta] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [detalleEliminar, setDetalleEliminar] = useState(null);

  const cargarDatos = async () => {
    try {
      const [
        respuestaDetalles,
        respuestaVentas,
        respuestaFunciones,
        respuestaUsuarios,
        respuestaPeliculas,
        respuestaSalas,
      ] = await Promise.all([
        api.get("/detalles-venta/"),
        api.get("/ventas/"),
        api.get("/funciones/"),
        api.get("/usuarios/"),
        api.get("/peliculas/"),
        api.get("/salas/"),
      ]);

      setDetalles(respuestaDetalles.data);
      setVentas(respuestaVentas.data);
      setFunciones(respuestaFunciones.data);
      setUsuarios(respuestaUsuarios.data);
      setPeliculas(respuestaPeliculas.data);
      setSalas(respuestaSalas.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar los boletos",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const ventasPorId = useMemo(
    () => new Map(ventas.map((venta) => [venta.id, venta])),
    [ventas],
  );

  const funcionesPorId = useMemo(
    () => new Map(funciones.map((funcion) => [funcion.id, funcion])),
    [funciones],
  );

  const usuariosPorId = useMemo(
    () => new Map(usuarios.map((usuario) => [usuario.id, usuario])),
    [usuarios],
  );

  const peliculasPorId = useMemo(
    () => new Map(peliculas.map((pelicula) => [pelicula.id, pelicula])),
    [peliculas],
  );

  const salasPorId = useMemo(
    () => new Map(salas.map((sala) => [sala.id, sala])),
    [salas],
  );

  const descripcionVenta = (venta) => {
    const usuario = usuariosPorId.get(venta?.id_usuario);
    return `Venta ${venta?.id ?? "-"} - ${usuario?.nombres_usuario ?? `Usuario ${venta?.id_usuario ?? "-"}`}`;
  };

  const descripcionFuncion = (funcion) => {
    if (!funcion) {
      return "Funcion sin seleccionar";
    }

    const pelicula = peliculasPorId.get(funcion.id_pelicula);
    const sala = salasPorId.get(funcion.id_sala);
    return `${pelicula?.titulo ?? `Pelicula ${funcion.id_pelicula}`} - ${
      sala?.nombre_sala ?? `Sala ${funcion.id_sala}`
    } - ${funcion.fecha_funcion} ${String(funcion.hora).slice(0, 5)}`;
  };

  const limpiarFormulario = () => {
    setIdEditar(null);
    setIdVenta("");
    setIdFuncion("");
    setAsiento("");
    setCodigoBoleto("");
  };

  const validarFormulario = () => {
    if (!idVenta || !idFuncion || asiento.trim() === "" || codigoBoleto.trim() === "") {
      setMensaje(mensajeInfo("Campos incompletos", "Complete venta, funcion, asiento y codigo."));
      return false;
    }

    if (asiento.trim().length < 2) {
      setMensaje(mensajeInfo("Asiento invalido", "Ingrese un asiento como A1, B10 o C7."));
      return false;
    }

    return true;
  };

  const datosDetalle = () => ({
    id_venta: Number(idVenta),
    id_funcion: Number(idFuncion),
    asiento: asiento.trim().toUpperCase(),
    codigo_boleto: codigoBoleto.trim().toUpperCase(),
  });

  const guardarDetalle = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.post("/detalles-venta/", datosDetalle());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Boleto registrado correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "El boleto no pudo registrarse."),
        ),
      );
    }
  };

  const editarDetalle = (detalle) => {
    setIdEditar(detalle.id);
    setIdVenta(String(detalle.id_venta));
    setIdFuncion(String(detalle.id_funcion));
    setAsiento(detalle.asiento);
    setCodigoBoleto(detalle.codigo_boleto);
    setMensaje(null);
  };

  const actualizarDetalle = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.put(`/detalles-venta/${idEditar}`, datosDetalle());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Boleto actualizado correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "El boleto no pudo actualizarse."),
        ),
      );
    }
  };

  const eliminarDetalle = async () => {
    if (!detalleEliminar) {
      return;
    }

    try {
      await api.delete(`/detalles-venta/${detalleEliminar.id}`);
      await cargarDatos();
      setDetalleEliminar(null);
      setMensaje(mensajeExito("Boleto eliminado", "El registro fue eliminado correctamente."));
    } catch (error) {
      setDetalleEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "El boleto no pudo eliminarse."),
        ),
      );
    }
  };

  const cargarDetallesPorVenta = async (ventaId) => {
    setFiltroVenta(ventaId);

    if (!ventaId) {
      await cargarDatos();
      return;
    }

    try {
      const respuesta = await api.get(`/detalles-venta/venta/${ventaId}`);
      setDetalles(respuesta.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo filtrar",
          obtenerMensajeError(error, "No se pudieron cargar los boletos de la venta."),
        ),
      );
    }
  };

  const detallesFiltrados = detalles.filter((detalle) => {
    const venta = ventasPorId.get(detalle.id_venta);
    const usuario = usuariosPorId.get(venta?.id_usuario);
    const funcion = funcionesPorId.get(detalle.id_funcion);
    const pelicula = peliculasPorId.get(funcion?.id_pelicula);
    const sala = salasPorId.get(funcion?.id_sala);
    const texto = busqueda.toLowerCase();
    const resumen = [
      detalle.codigo_boleto,
      detalle.asiento,
      usuario?.nombres_usuario,
      pelicula?.titulo,
      sala?.nombre_sala,
      funcion?.fecha_funcion,
    ]
      .join(" ")
      .toLowerCase();

    return resumen.includes(texto);
  });

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Boletos" />

        <div className="page-content detalles-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-ticket-perforated-fill"} me-2`}></i>
                    {idEditar ? "Editar Boleto" : "Registrar Boleto"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="ventaDetalle">
                      Venta
                    </label>
                    <select
                      id="ventaDetalle"
                      className="form-select"
                      value={idVenta}
                      onChange={(event) => setIdVenta(event.target.value)}
                    >
                      <option value="">Seleccionar venta</option>
                      {ventas.map((venta) => (
                        <option key={venta.id} value={venta.id}>
                          {descripcionVenta(venta)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="funcionDetalle">
                      Funcion
                    </label>
                    <select
                      id="funcionDetalle"
                      className="form-select"
                      value={idFuncion}
                      onChange={(event) => setIdFuncion(event.target.value)}
                    >
                      <option value="">Seleccionar funcion</option>
                      {funciones.map((funcion) => (
                        <option key={funcion.id} value={funcion.id}>
                          {descripcionFuncion(funcion)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="row">
                    <div className="col-md-5 mb-3">
                      <label className="form-label" htmlFor="asientoDetalle">
                        Asiento
                      </label>
                      <input
                        id="asientoDetalle"
                        className="form-control"
                        value={asiento}
                        onChange={(event) => setAsiento(event.target.value)}
                        placeholder="A1"
                      />
                    </div>

                    <div className="col-md-7 mb-3">
                      <label className="form-label" htmlFor="codigoDetalle">
                        Codigo
                      </label>
                      <input
                        id="codigoDetalle"
                        className="form-control"
                        value={codigoBoleto}
                        onChange={(event) => setCodigoBoleto(event.target.value)}
                        placeholder="BOL-001"
                      />
                    </div>
                  </div>

                  {idFuncion && (
                    <div className="datos-resumen mb-3">
                      <span>
                        <strong>Funcion:</strong>{" "}
                        {descripcionFuncion(funcionesPorId.get(Number(idFuncion)))}
                      </span>
                      <span>
                        <strong>Precio:</strong> S/.{" "}
                        {Number(funcionesPorId.get(Number(idFuncion))?.precio ?? 0).toFixed(2)}
                      </span>
                    </div>
                  )}

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarDetalle : guardarDetalle}
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
                <div className="card-header boletos-header">
                  <h5>
                    <i className="bi bi-ticket-detailed-fill me-2"></i>
                    Boletos registrados
                  </h5>

                  <select
                    className="form-select filtro-venta"
                    value={filtroVenta}
                    onChange={(event) => cargarDetallesPorVenta(event.target.value)}
                  >
                    <option value="">Todas las ventas</option>
                    {ventas.map((venta) => (
                      <option key={venta.id} value={venta.id}>
                        {descripcionVenta(venta)}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <div className="input-group">
                      <span className="input-group-text">
                        <i className="bi bi-search"></i>
                      </span>
                      <input
                        className="form-control"
                        placeholder="Buscar por codigo, asiento, usuario o pelicula..."
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
                          <th>Codigo</th>
                          <th>Usuario</th>
                          <th>Pelicula</th>
                          <th>Sala</th>
                          <th>Asiento</th>
                          <th>Precio</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {detallesFiltrados.length === 0 ? (
                          <tr>
                            <td colSpan="8" className="empty-row">
                              {detalles.length === 0
                                ? "No existen boletos registrados"
                                : "No se encontraron boletos con esa busqueda"}
                            </td>
                          </tr>
                        ) : (
                          detallesFiltrados.map((detalle) => {
                            const venta = ventasPorId.get(detalle.id_venta);
                            const usuario = usuariosPorId.get(venta?.id_usuario);
                            const funcion = funcionesPorId.get(detalle.id_funcion);
                            const pelicula = peliculasPorId.get(funcion?.id_pelicula);
                            const sala = salasPorId.get(funcion?.id_sala);

                            return (
                              <tr key={detalle.id}>
                                <td>{detalle.id}</td>
                                <td>{detalle.codigo_boleto}</td>
                                <td>{usuario?.nombres_usuario ?? `Usuario ${venta?.id_usuario ?? "-"}`}</td>
                                <td>{pelicula?.titulo ?? `Pelicula ${funcion?.id_pelicula ?? "-"}`}</td>
                                <td>{sala?.nombre_sala ?? `Sala ${funcion?.id_sala ?? "-"}`}</td>
                                <td>
                                  <span className="badge badge-soft">{detalle.asiento}</span>
                                </td>
                                <td>S/. {Number(funcion?.precio ?? 0).toFixed(2)}</td>
                                <td>
                                  <div className="acciones-tabla">
                                    <button
                                      type="button"
                                      className="btn btn-warning btn-sm"
                                      onClick={() => editarDetalle(detalle)}
                                      title="Editar boleto"
                                    >
                                      <i className="bi bi-pencil-square"></i>
                                    </button>

                                    <button
                                      type="button"
                                      className="btn btn-danger btn-sm"
                                      onClick={() => setDetalleEliminar(detalle)}
                                      title="Eliminar boleto"
                                    >
                                      <i className="bi bi-trash-fill"></i>
                                    </button>
                                  </div>
                                </td>
                              </tr>
                            );
                          })
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
        abierta={Boolean(detalleEliminar)}
        titulo="Eliminar boleto"
        mensaje={`Se eliminara el boleto ${detalleEliminar?.codigo_boleto ?? "seleccionado"}.`}
        textoConfirmar="Eliminar"
        onCancelar={() => setDetalleEliminar(null)}
        onConfirmar={eliminarDetalle}
      />
    </>
  );
}

export default DetallesVenta;
