import { Link } from "react-router-dom";
import { useState } from "react";

import logo from "../../assets/imagenes/logo.svg";
import "./menu.css";

function Menu() {
  const [menuAbierto, setMenuAbierto] = useState(false);

  const cerrarMenu = () => {
    setMenuAbierto(false);
  };

  return (
    <>
      <button
        type="button"
        className="boton-menu"
        onClick={() => setMenuAbierto(!menuAbierto)}
        aria-label="Abrir menu"
      >
        <i className={menuAbierto ? "bi bi-x-lg" : "bi bi-list"}></i>
      </button>

      <aside className={`sidebar ${menuAbierto ? "menu-abierto" : ""}`}>
        <div className="logo-container">
          <Link to="/dashboard" onClick={cerrarMenu}>
            <img src={logo} alt="Cinemax" className="logo" />
          </Link>

          <h2>CINEMAX</h2>
          <p>Sistema de gestion de cine</p>
        </div>

        <nav>
          <ul>
            <li>
              <Link to="/dashboard" onClick={cerrarMenu}>
                <i className="bi bi-speedometer2"></i>
                <span>Inicio</span>
              </Link>
            </li>

            <li>
              <Link to="/usuarios" onClick={cerrarMenu}>
                <i className="bi bi-people-fill"></i>
                <span>Usuarios</span>
              </Link>
            </li>

            <li>
              <Link to="/peliculas" onClick={cerrarMenu}>
                <i className="bi bi-film"></i>
                <span>Peliculas</span>
              </Link>
            </li>

            <li>
              <Link to="/salas" onClick={cerrarMenu}>
                <i className="bi bi-grid-3x3-gap-fill"></i>
                <span>Salas</span>
              </Link>
            </li>

            <li>
              <Link to="/funciones" onClick={cerrarMenu}>
                <i className="bi bi-calendar-event-fill"></i>
                <span>Funciones</span>
              </Link>
            </li>

            <li>
              <Link to="/ventas" onClick={cerrarMenu}>
                <i className="bi bi-receipt-cutoff"></i>
                <span>Ventas</span>
              </Link>
            </li>

            <li>
              <Link to="/detalles-venta" onClick={cerrarMenu}>
                <i className="bi bi-ticket-perforated-fill"></i>
                <span>Boletos</span>
              </Link>
            </li>

            <li>
              <Link to="/registros" onClick={cerrarMenu}>
                <i className="bi bi-clock-history"></i>
                <span>Registros</span>
              </Link>
            </li>
          </ul>
        </nav>
      </aside>
    </>
  );
}

export default Menu;
