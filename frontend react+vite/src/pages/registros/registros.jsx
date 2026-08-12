import { useEffect, useMemo, useState } from "react";

import api from "../../api/axios";
import Confirmacion from "../../components/confirmacion/confirmacion";
import Header from "../../components/header/header";
import Mensaje from "../../components/mensaje/mensaje";
import Menu from "../../components/menu/menu";
import {
  mensajeError,
  mensajeExito,
  obtenerMensajeError,
} from "../../utils/mensajes";
import "./registros.css";

const modulos = [
  "Todos",
  "Usuarios",
  "Peliculas",
  "Salas",
  "Funciones",
  "Ventas",
  "Detalles de venta",
  "Sistema",
];

const acciones = ["Todas", "Registrar", "Actualizar", "Eliminar", "Informacion"];

function Registros() {
  const [registros, setRegistros] = useState([]);
  const [filtroModulo, setFiltroModulo] = useState("Todos");
  const [filtroAccion, setFiltroAccion] = useState("Todas");
  const [busqueda, setBusqueda] = useState("");
  const [mostrarConfirmacion, setMostrarConfirmacion] = useState(false);
  const [mensaje, setMensaje] = useState(null);

  const cargarRegistros = async () => {
    try {
      const respuesta = await api.get("/registros/");
      setRegistros(respuesta.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo cargar el historial",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarRegistros();
  }, []);

  const limpiarFiltros = () => {
    setFiltroModulo("Todos");
    setFiltroAccion("Todas");
    setBusqueda("");
  };

  const eliminarHistorial = async () => {
    try {
      await api.delete("/registros/");
      setRegistros([]);
      setMostrarConfirmacion(false);
      setMensaje(mensajeExito("Historial limpio", "Los registros fueron eliminados correctamente."));
    } catch (error) {
      setMostrarConfirmacion(false);
      setMensaje(
        mensajeError(
          "No se pudo limpiar",
          obtenerMensajeError(error, "No se pudo eliminar el historial."),
        ),
      );
    }
  };

  const registrosFiltrados = useMemo(
    () =>
      registros.filter((registro) => {
        const coincideModulo = filtroModulo === "Todos" || registro.modulo === filtroModulo;
        const coincideAccion = filtroAccion === "Todas" || registro.accion === filtroAccion;
        const texto = [
          registro.hora,
          registro.nivel,
          registro.modulo,
          registro.accion,
          registro.informacion,
        ]
          .join(" ")
          .toLowerCase();

        return coincideModulo && coincideAccion && texto.includes(busqueda.toLowerCase());
      }),
    [busqueda, filtroAccion, filtroModulo, registros],
  );

  const claseAccion = (accion) => {
    if (accion === "Registrar") {
      return "bg-success";
    }

    if (accion === "Actualizar") {
      return "bg-primary";
    }

    if (accion === "Eliminar") {
      return "bg-danger";
    }

    return "bg-secondary";
  };

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Registros" />

        <div className="page-content registros">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="card shadow">
            <div className="card-header registros-header">
              <div>
                <h4>
                  <i className="bi bi-clock-history me-2"></i>
                  Historial
                </h4>
                <p>Historial de actividades del sistema Cinemax</p>
              </div>

              <span className="badge badge-soft">{registrosFiltrados.length} registros</span>
            </div>

            <div className="card-body">
              <div className="filtros-linea mb-4">
                <div>
                  <label className="form-label" htmlFor="filtroModulo">
                    Modulo
                  </label>
                  <select
                    id="filtroModulo"
                    className="form-select"
                    value={filtroModulo}
                    onChange={(event) => setFiltroModulo(event.target.value)}
                  >
                    {modulos.map((modulo) => (
                      <option key={modulo} value={modulo}>
                        {modulo}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="form-label" htmlFor="filtroAccion">
                    Accion
                  </label>
                  <select
                    id="filtroAccion"
                    className="form-select"
                    value={filtroAccion}
                    onChange={(event) => setFiltroAccion(event.target.value)}
                  >
                    {acciones.map((accion) => (
                      <option key={accion} value={accion}>
                        {accion}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="form-label" htmlFor="busquedaRegistros">
                    Buscar
                  </label>
                  <input
                    id="busquedaRegistros"
                    className="form-control"
                    placeholder="Buscar en los registros..."
                    value={busqueda}
                    onChange={(event) => setBusqueda(event.target.value)}
                  />
                </div>

                <div className="acciones-registros">
                  <button type="button" className="btn btn-secondary" onClick={limpiarFiltros}>
                    <i className="bi bi-eraser-fill me-2"></i>
                    Limpiar
                  </button>

                  <button
                    type="button"
                    className="btn btn-outline-danger"
                    onClick={() => setMostrarConfirmacion(true)}
                  >
                    <i className="bi bi-trash-fill me-2"></i>
                    Historial
                  </button>
                </div>
              </div>

              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th className="text-center">Hora</th>
                      <th className="text-center">Nivel</th>
                      <th className="text-center">Modulo</th>
                      <th className="text-center">Accion</th>
                      <th className="text-center">Informacion</th>
                    </tr>
                  </thead>

                  <tbody>
                    {registrosFiltrados.length === 0 ? (
                      <tr>
                        <td colSpan="5" className="empty-row">
                          No existen registros con los filtros seleccionados
                        </td>
                      </tr>
                    ) : (
                      registrosFiltrados.map((registro, index) => (
                        <tr key={`${registro.hora}-${index}`}>
                          <td className="text-center">{registro.hora}</td>
                          <td className="text-center">{registro.nivel}</td>
                          <td className="text-center">{registro.modulo}</td>
                          <td className="text-center">
                            <span className={`badge ${claseAccion(registro.accion)}`}>
                              {registro.accion}
                            </span>
                          </td>
                          <td>{registro.informacion}</td>
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

      <Confirmacion
        abierta={mostrarConfirmacion}
        titulo="Limpiar historial"
        mensaje="Se eliminaran todos los registros de actividad del backend."
        textoConfirmar="Limpiar"
        onCancelar={() => setMostrarConfirmacion(false)}
        onConfirmar={eliminarHistorial}
      />
    </>
  );
}

export default Registros;
