function Confirmacion({
  abierta,
  titulo,
  mensaje,
  textoConfirmar = "Confirmar",
  textoCancelar = "Cancelar",
  onCancelar,
  onConfirmar,
}) {
  if (!abierta) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-confirmacion">
        <div className="modal-icono">
          <i className="bi bi-exclamation-triangle-fill"></i>
        </div>

        <h3>{titulo}</h3>
        <p>{mensaje}</p>

        <div className="modal-botones">
          <button type="button" className="btn btn-secondary" onClick={onCancelar}>
            {textoCancelar}
          </button>

          <button type="button" className="btn btn-danger" onClick={onConfirmar}>
            {textoConfirmar}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Confirmacion;
