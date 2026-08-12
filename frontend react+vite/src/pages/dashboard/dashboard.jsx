import { Link } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";

import api from "../../api/axios";
import Header from "../../components/header/header";
import Mensaje from "../../components/mensaje/mensaje";
import Menu from "../../components/menu/menu";
import { mensajeError, obtenerMensajeError } from "../../utils/mensajes";
import "./dashboard.css";

function Dashboard() {
  const [usuarios, setUsuarios] = useState([]);
  const [peliculas, setPeliculas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [funciones, setFunciones] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [detalles, setDetalles] = useState([]);
  const [mensaje, setMensaje] = useState(null);

  useEffect(() => {
    const cargarDashboard = async () => {
      try {
        const [
          respuestaUsuarios,
          respuestaPeliculas,
          respuestaSalas,
          respuestaFunciones,
          respuestaVentas,
          respuestaDetalles,
        ] = await Promise.all([
          api.get("/usuarios/"),
          api.get("/peliculas/"),
          api.get("/salas/"),
          api.get("/funciones/"),
          api.get("/ventas/"),
          api.get("/detalles-venta/"),
        ]);

        setUsuarios(respuestaUsuarios.data);
        setPeliculas(respuestaPeliculas.data);
        setSalas(respuestaSalas.data);
        setFunciones(respuestaFunciones.data);
        setVentas(respuestaVentas.data);
        setDetalles(respuestaDetalles.data);
      } catch (error) {
        setMensaje(
          mensajeError(
            "No se pudo cargar el dashboard",
            obtenerMensajeError(error, "Revise que el backend de Cinemax este activo."),
          ),
        );
      }
    };

    cargarDashboard();
  }, []);

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

  const funcionesPorId = useMemo(
    () => new Map(funciones.map((funcion) => [funcion.id, funcion])),
    [funciones],
  );

  const ingresos = detalles.reduce((total, detalle) => {
    const funcion = funcionesPorId.get(detalle.id_funcion);
    return total + Number(funcion?.precio ?? 0);
  }, 0);

  const ultimosBoletos = detalles.slice(-5).reverse();

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Dashboard" />

        <div className="page-content">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <section className="dashboard">
            <Link to="/usuarios" className="card-link">
              <div className="card-dashboard card-usuarios">
                <i className="bi bi-people-fill"></i>
                <h5>Usuarios</h5>
                <h2>{usuarios.length}</h2>
              </div>
            </Link>

            <Link to="/peliculas" className="card-link">
              <div className="card-dashboard card-peliculas">
                <i className="bi bi-film"></i>
                <h5>Peliculas</h5>
                <h2>{peliculas.length}</h2>
              </div>
            </Link>

            <Link to="/funciones" className="card-link">
              <div className="card-dashboard card-funciones">
                <i className="bi bi-calendar-event-fill"></i>
                <h5>Funciones</h5>
                <h2>{funciones.length}</h2>
              </div>
            </Link>

            <div className="card-dashboard card-ingresos">
              <i className="bi bi-cash-stack"></i>
              <h5>Ingresos</h5>
              <h2>S/. {ingresos.toFixed(2)}</h2>
            </div>
          </section>

          <section className="tabla-dashboard">
            <div className="card shadow">
              <div className="card-header">
                <h5>
                  <i className="bi bi-ticket-perforated-fill me-2"></i>
                  Ultimos boletos vendidos
                </h5>
              </div>

              <div className="card-body">
                <div className="table-responsive">
                  <table className="table table-hover">
                    <thead>
                      <tr>
                        <th className="text-center">ID</th>
                        <th className="text-center">Usuario</th>
                        <th className="text-center">Pelicula</th>
                        <th className="text-center">Sala</th>
                        <th className="text-center">Asiento</th>
                        <th className="text-center">Precio</th>
                      </tr>
                    </thead>

                    <tbody>
                      {ultimosBoletos.length === 0 ? (
                        <tr>
                          <td colSpan="6" className="empty-row">
                            No existen boletos registrados
                          </td>
                        </tr>
                      ) : (
                        ultimosBoletos.map((detalle) => {
                          const venta = ventas.find((item) => item.id === detalle.id_venta);
                          const usuario = usuariosPorId.get(venta?.id_usuario);
                          const funcion = funcionesPorId.get(detalle.id_funcion);
                          const pelicula = peliculasPorId.get(funcion?.id_pelicula);
                          const sala = salasPorId.get(funcion?.id_sala);

                          return (
                            <tr key={detalle.id}>
                              <td className="text-center">{detalle.id}</td>
                              <td className="text-center">
                                {usuario?.nombres_usuario ?? `Usuario ${venta?.id_usuario ?? "-"}`}
                              </td>
                              <td className="text-center">
                                {pelicula?.titulo ?? `Pelicula ${funcion?.id_pelicula ?? "-"}`}
                              </td>
                              <td className="text-center">
                                {sala?.nombre_sala ?? `Sala ${funcion?.id_sala ?? "-"}`}
                              </td>
                              <td className="text-center">{detalle.asiento}</td>
                              <td className="text-center">
                                S/. {Number(funcion?.precio ?? 0).toFixed(2)}
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
          </section>
        </div>
      </div>
    </>
  );
}

export default Dashboard;
