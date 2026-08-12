import { useState } from "react";
import { useNavigate } from "react-router-dom";

import logo from "../../assets/imagenes/logo.svg";
import Mensaje from "../../components/mensaje/mensaje";
import { mensajeError } from "../../utils/mensajes";
import "./login.css";

function Login() {
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [mensaje, setMensaje] = useState(null);

  const ingresar = (event) => {
    event.preventDefault();

    if (usuario.trim().toLowerCase() === "admin" && contrasena === "admin123") {
      navigate("/dashboard");
      return;
    }

    setMensaje(
      mensajeError(
        "Acceso denegado",
        "El usuario o la contrasena no corresponde al administrador.",
      ),
    );
  };

  return (
    <main className="login-container">
      <section className="login-panel">
        <div className="login-marca">
          <img src={logo} alt="Cinemax" className="login-logo" />
          <h1>CINEMAX</h1>
          <p>Sistema de Gestion de Cine</p>
        </div>

        <div className="login-formulario">
          <h2>Iniciar sesion</h2>
          <Mensaje mensaje={mensaje} onClose={() => setMensaje(null)} />

          <form onSubmit={ingresar}>
            <div className="mb-3">
              <label htmlFor="usuario">Usuario</label>
              <input
                id="usuario"
                className="form-control"
                placeholder="Ingrese su usuario"
                value={usuario}
                onChange={(event) => setUsuario(event.target.value)}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="contrasena">Contrasena</label>
              <input
                id="contrasena"
                type="password"
                className="form-control"
                placeholder="Ingrese su contrasena"
                value={contrasena}
                onChange={(event) => setContrasena(event.target.value)}
              />
            </div>

            <button type="submit" className="btn btn-primary w-100">
              <i className="bi bi-box-arrow-in-right me-2"></i>
              Entrar
            </button>
          </form>
        </div>
      </section>
    </main>
  );
}

export default Login;
