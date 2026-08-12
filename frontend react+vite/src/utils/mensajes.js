export const mensajeExito = (titulo, texto) => ({
  tipo: "ok",
  titulo,
  texto,
});

export const mensajeError = (titulo, texto) => ({
  tipo: "error",
  titulo,
  texto,
});

export const mensajeInfo = (titulo, texto) => ({
  tipo: "info",
  titulo,
  texto,
});

export const obtenerMensajeError = (error, textoPorDefecto) => {
  const detalle = error?.response?.data?.detail;

  if (Array.isArray(detalle)) {
    return detalle.map((item) => item?.msg ?? String(item)).join(" ");
  }

  if (typeof detalle === "string") {
    return detalle;
  }

  return textoPorDefecto;
};
