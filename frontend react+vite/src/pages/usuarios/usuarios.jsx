import { useEffect, useState } from "react";

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
import "./usuarios.css";

function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [nombresUsuario, setNombresUsuario] = useState("");
  const [correo, setCorreo] = useState("");
  const [idEditar, setIdEditar] = useState(null);
  const [busqueda, setBusqueda] = useState("");
  const [mensaje, setMensaje] = useState(null);
  const [usuarioEliminar, setUsuarioEliminar] = useState(null);

  const cargarUsuarios = async () => {
    try {
      const respuesta = await api.get("/usuarios/");
      setUsuarios(respuesta.data);
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudieron cargar los usuarios",
          obtenerMensajeError(error, "Revise que el backend este activo."),
        ),
      );
    }
  };

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const limpiarFormulario = () => {
    setIdEditar(null);
    setNombresUsuario("");
    setCorreo("");
  };

  const validarFormulario = () => {
    if (nombresUsuario.trim() === "" || correo.trim() === "") {
      setMensaje(mensajeInfo("Campos incompletos", "Complete el nombre y el correo."));
      return false;
    }

    if (!correo.includes("@") || !correo.includes(".")) {
      setMensaje(mensajeInfo("Correo invalido", "Ingrese un correo con formato valido."));
      return false;
    }

    return true;
  };

  const guardarUsuario = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.post("/usuarios/", {
        nombres_usuario: nombresUsuario.trim(),
        correo: correo.trim(),
      });

      await cargarUsuarios();
      limpiarFormulario();
      setMensaje(mensajeExito("Registro exitoso", "Usuario registrado correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo registrar",
          obtenerMensajeError(error, "El usuario no pudo registrarse."),
        ),
      );
    }
  };

  const editarUsuario = (usuario) => {
    setIdEditar(usuario.id);
    setNombresUsuario(usuario.nombres_usuario);
    setCorreo(usuario.correo);
    setMensaje(null);
  };

  const actualizarUsuario = async () => {
    if (!validarFormulario()) {
      return;
    }

    try {
      await api.put(`/usuarios/${idEditar}`, {
        nombres_usuario: nombresUsuario.trim(),
        correo: correo.trim(),
      });

      await cargarUsuarios();
      limpiarFormulario();
      setMensaje(mensajeExito("Actualizacion exitosa", "Usuario actualizado correctamente."));
    } catch (error) {
      setMensaje(
        mensajeError(
          "No se pudo actualizar",
          obtenerMensajeError(error, "El usuario no pudo actualizarse."),
        ),
      );
    }
  };

  const eliminarUsuario = async () => {
    if (!usuarioEliminar) {
      return;
    }

    try {
      await api.delete(`/usuarios/${usuarioEliminar.id}`);
      await cargarUsuarios();
      setUsuarioEliminar(null);
      setMensaje(mensajeExito("Usuario eliminado", "El registro fue eliminado correctamente."));
    } catch (error) {
      setUsuarioEliminar(null);
      setMensaje(
        mensajeError(
          "No se pudo eliminar",
          obtenerMensajeError(error, "El usuario tiene informacion relacionada."),
        ),
      );
    }
  };

  const usuariosFiltrados = usuarios.filter((usuario) => {
    const texto = busqueda.toLowerCase();
    return (
      usuario.nombres_usuario.toLowerCase().includes(texto) ||
      usuario.correo.toLowerCase().includes(texto)
    );
  });

  return (
    <>
      <Menu />
      <div className="contenido">
        <Header titulo="Usuarios" />

        <div className="page-content usuarios-contenido">
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <div className="row module-grid g-4">
            <div className="col-lg-4">
              <div className="card shadow">
                <div className="card-header">
                  <h5>
                    <i className={`bi ${idEditar ? "bi-pencil-square" : "bi-person-plus-fill"} me-2`}></i>
                    {idEditar ? "Editar Usuario" : "Registrar Usuario"}
                  </h5>
                </div>

                <div className="card-body">
                  <div className="mb-3">
                    <label className="form-label" htmlFor="nombresUsuario">
                      Nombres
                    </label>
                    <input
                      id="nombresUsuario"
                      className="form-control"
                      value={nombresUsuario}
                      onChange={(event) => setNombresUsuario(event.target.value)}
                      placeholder="Nombre del usuario"
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label" htmlFor="correoUsuario">
                      Correo
                    </label>
                    <input
                      id="correoUsuario"
                      type="email"
                      className="form-control"
                      value={correo}
                      onChange={(event) => setCorreo(event.target.value)}
                      placeholder="usuario@correo.com"
                    />
                  </div>

                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={idEditar ? actualizarUsuario : guardarUsuario}
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
                    <i className="bi bi-people-fill me-2"></i>
                    Usuarios registrados
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
                        placeholder="Buscar por nombre o correo..."
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
                          <th>Nombres</th>
                          <th>Correo</th>
                          <th>Acciones</th>
                        </tr>
                      </thead>

                      <tbody>
                        {usuariosFiltrados.length === 0 ? (
                          <tr>
                            <td colSpan="4" className="empty-row">
                              {usuarios.length === 0
                                ? "No existen usuarios registrados"
                                : "No se encontraron usuarios con esa busqueda"}
                            </td>
                          </tr>
                        ) : (
                          usuariosFiltrados.map((usuario) => (
                            <tr key={usuario.id}>
                              <td>{usuario.id}</td>
                              <td>{usuario.nombres_usuario}</td>
                              <td>{usuario.correo}</td>
                              <td>
                                <div className="acciones-tabla">
                                  <button
                                    type="button"
                                    className="btn btn-warning btn-sm"
                                    onClick={() => editarUsuario(usuario)}
                                    title="Editar usuario"
                                  >
                                    <i className="bi bi-pencil-square"></i>
                                  </button>

                                  <button
                                    type="button"
                                    className="btn btn-danger btn-sm"
                                    onClick={() => setUsuarioEliminar(usuario)}
                                    title="Eliminar usuario"
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
        abierta={Boolean(usuarioEliminar)}
        titulo="Eliminar usuario"
        mensaje={`Se eliminara ${usuarioEliminar?.nombres_usuario ?? "este usuario"} del sistema.`}
        textoConfirmar="Eliminar"
        onCancelar={() => setUsuarioEliminar(null)}
        onConfirmar={eliminarUsuario}
      />
    </>
  );
}

export default Usuarios;
