import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Confirmacion from "../confirmacion/confirmacion";
import "./header.css";

function Header({ titulo }) {
  const [hora, setHora] = useState(new Date());
  const [mostrarConfirmacion, setMostrarConfirmacion] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const intervalo = setInterval(() => {
      setHora(new Date());
    }, 1000);

    return () => clearInterval(intervalo);
  }, []);

  const cerrarSesion = () => {
    setMostrarConfirmacion(false);
    navigate("/");
  };

  return (
    <>
      <header className="header">
        <div>
          <h2>{titulo}</h2>
          <p>Bienvenido al Sistema de Gestion de Cine Cinemax</p>
        </div>

        <button
          type="button"
          className="usuario"
          onClick={() => setMostrarConfirmacion(true)}
        >
          <i className="bi bi-person-circle"></i>
          <span>Administrador</span>
          <span className="hora">{hora.toLocaleTimeString()}</span>
        </button>
      </header>

      <Confirmacion
        abierta={mostrarConfirmacion}
        titulo="Cerrar sesion"
        mensaje="Confirma que deseas salir del sistema."
        textoConfirmar="Cerrar sesion"
        onCancelar={() => setMostrarConfirmacion(false)}
        onConfirmar={cerrarSesion}
      />
    </>
  );
}

export default Header;
