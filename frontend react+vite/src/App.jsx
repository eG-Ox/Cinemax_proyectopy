import { Navigate, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/dashboard/dashboard";
import DetallesVenta from "./pages/detalles/detalles";
import Funciones from "./pages/funciones/funciones";
import Login from "./pages/login/login";
import Peliculas from "./pages/peliculas/peliculas";
import Registros from "./pages/registros/registros";
import Salas from "./pages/salas/salas";
import Usuarios from "./pages/usuarios/usuarios";
import Ventas from "./pages/ventas/ventas";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/usuarios" element={<Usuarios />} />
      <Route path="/peliculas" element={<Peliculas />} />
      <Route path="/salas" element={<Salas />} />
      <Route path="/funciones" element={<Funciones />} />
      <Route path="/ventas" element={<Ventas />} />
      <Route path="/detalles-venta" element={<DetallesVenta />} />
      <Route path="/registros" element={<Registros />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
