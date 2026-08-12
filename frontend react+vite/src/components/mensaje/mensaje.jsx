function Mensaje({ mensaje, onClose }) {
  if (!mensaje) {
    return null;
  }

  return (
    <div className={`mensaje mensaje-${mensaje.tipo}`} role="status">
      <div>
        <h6>{mensaje.titulo}</h6>
        <p>{mensaje.texto}</p>
      </div>

      {onClose && (
        <button
          type="button"
          className="mensaje-cerrar"
          onClick={onClose}
          aria-label="Cerrar mensaje"
        >
          <i className="bi bi-x-lg"></i>
        </button>
      )}
    </div>
  );
}

export default Mensaje;
