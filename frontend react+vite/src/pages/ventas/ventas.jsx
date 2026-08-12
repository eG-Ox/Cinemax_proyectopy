import { useEffect, useMemo, useState } from "react";

import api from "../../api/axios";
import Header from "../../components/header/header";
import Mensaje from "../../components/mensaje/mensaje";
import Menu from "../../components/menu/menu";
import { mensajeError, obtenerMensajeError } from "../../utils/mensajes";
import "./ventas.css";

function Ventas() {
  const [ventas, setVentas] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [filtroUsuario, setFiltroUsuario] = useState("");
  const [mensaje, setMensaje] = useState(null);

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
            <div className="col-12">
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
                          <th>Total</th>
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
                              <td>S/. {Number(venta.total ?? 0).toFixed(2)}</td>
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
    </>
  );
}

export default Ventas;
