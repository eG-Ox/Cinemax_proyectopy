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
import "./ventas.css";

const formatearFechaLocal = (fecha) => {
  if (!fecha) {
    return "";
  }

  return String(fecha).slice(0, 16);
};

function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [idUsuario, setIdUsuario] = useState("");
  const [fechaCompra, setFechaCompra] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [filtroUsuario, setFiltroUsuario] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [ventaEliminar, setVentaEliminar] = useState(null);

  const cargarDatos = async () => {
    try {
      const [respuestaVentas, respuestaUsuarios] = await Promise.all([
        api.get("/ventas/"),
        api.get("/usuarios/"),
      ]);

      setVentas(respuestaVentas.data);
      setUsuarios(respuestaUsuarios.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar las ventas",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  const usuariosPorId = useMemo(
    () => new Map(usuarios.map((usuario) => [usuario.id, usuario])),
    [usuarios],
  );

  const limpiarFormulario = () => {
    setIdEditar(null);
    setIdUsuario("");
    setFechaCompra("");
  };

  const validarFormulario = () => {
    if (!idUsuario) {
      setMensaje(mensajeInfo("Usuario requerido", "Seleccione el usuario de la venta."));
      return false;
    }

    return true;
  };

  const datosVenta = () => ({
    id_usuario: Number(idUsuario),
    fecha_compra: fechaCompra ? `${fechaCompra}:00` : undefined,
  });

  const guardarVenta = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.post("/ventas/", datosVenta());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Venta registrada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "La venta no pudo registrarse."),
        ),
      );
    }
  };

  const editarVenta = (venta) => {
    setIdEditar(venta.id);
    setIdUsuario(String(venta.id_usuario));
    setFechaCompra(formatearFechaLocal(venta.fecha_compra));
    setMensaje(null);
  };

  const actualizarVenta = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.put(`/ventas/${idEditar}`, datosVenta());
      await cargarDatos();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Venta actualizada correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "La venta no pudo actualizarse."),
        ),
      );
    }
  };

  const eliminarVenta = async () => {
    if (!ventaEliminar) {
      return;
    }

    try {
      await api.delete(`/ventas/${ventaEliminar.id}`);
      await cargarDatos();
      setVentaEliminar(null);
      setMensaje(mensajeExito("Venta eliminada", "El registro fue eliminado correctamente."));
    } catch (error) {
      setVentaEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "La venta tiene boletos asociados."),
        ),
      );
    }
  };

  const cargarVentasPorUsuario = async (usuarioId) => {
    setFiltroUsuario(usuarioId);

    if (!usuarioId) {
      await cargarDatos();
      return;
    }

    try {
      const respuesta = await api.get(`/ventas/usuario/${usuarioId}`);
      setVentas(respuesta.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo filtrar",
          obtenerMensajeError(error, "No se pudieron cargar las ventas del usuario."),
        ),
      );
    }
  };

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Ventas" />

        <div className="page-content ventas-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-receipt-cutoff"} me-2`}></i>
                    {idEditar ? "Editar Venta" : "Registrar Venta"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="usuarioVenta">
                      Usuario
                    </label>
                    <select
                      id="usuarioVenta"
                      className="form-select"
                      value={idUsuario}
                      onChange={(event) => setIdUsuario(event.target.value)}
                    >
                      <option value="">Seleccionar usuario</option>
                      {usuarios.map((usuario) => (
                        <option key={usuario.id} value={usuario.id}>
                          {usuario.nombres_usuario}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="fechaCompra">
                      Fecha de compra
                    </label>
                    <input
                      id="fechaCompra"
                      type="datetime-local"
                      className="form-control"
                      value={fechaCompra}
                      onChange={(event) => setFechaCompra(event.target.value)}
                    />
                  </div>

                  <div className="datos-resumen mb-3">
                    <span>
                      <strong>Fecha:</strong>{" "}
                      {fechaCompra || "El backend usara la fecha actual"}
                    </span>
                    <span>
                      <strong>Usuario:</strong>{" "}
                      {usuariosPorId.get(Number(idUsuario))?.nombres_usuario ?? "Sin seleccionar"}
                    </span>
                  </div>

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarVenta : guardarVenta}
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
                <div className="card-header ventas-header">
                  <h5>
                    <i className="bi bi-receipt me-2"></i>
                    Ventas registradas
                  </h5>

                  <select
                    className="form-select filtro-usuario"
                    value={filtroUsuario}
                    onChange={(event) => cargarVentasPorUsuario(event.target.value)}
                  >
                    <option value="">Todos los usuarios</option>
                    {usuarios.map((usuario) => (
                      <option key={usuario.id} value={usuario.id}>
                        {usuario.nombres_usuario}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="card-body">
                  <div className="table-responsive">
                    <table className="table table-hover">
                      <thead>
                        <tr>
                          <th>ID</th>
                          <th>Usuario</th>
                          <th>Fecha de compra</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {ventas.length === 0 ? (
                          <tr>
                            <td colSpan="4" className="empty-row">
                              No existen ventas registradas
                            </td>
                          </tr>
                        ) : (
                          ventas.map((venta) => (
                            <tr key={venta.id}>
                              <td>{venta.id}</td>
                              <td>
                                {usuariosPorId.get(venta.id_usuario)?.nombres_usuario ??
                                  `Usuario ${venta.id_usuario}`}
                              </td>
                              <td>{String(venta.fecha_compra).replace("T", " ")}</td>
                              <td>
                                <div className="acciones-tabla">
                                  <button
                                    type="button"
                                    className="btn btn-warning btn-sm"
                                    onClick={() => editarVenta(venta)}
                                    title="Editar venta"
                                  >
                                    <i className="bi bi-pencil-square"></i>
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-danger btn-sm"
                                    onClick={() => setVentaEliminar(venta)}
                                    title="Eliminar venta"
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
        abierta={Boolean(ventaEliminar)}
        titulo="Eliminar venta"
        mensaje="Se eliminara la venta seleccionada del sistema."
        textoConfirmar="Eliminar"
        onCancelar={() => setVentaEliminar(null)}
        onConfirmar={eliminarVenta}
      />
    </>
  );
}

export default Ventas;
