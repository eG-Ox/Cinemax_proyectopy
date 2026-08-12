CREATE TABLE IF NOT EXISTS usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombres_usuario TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS pelicula (
    id_pelicula SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    genero TEXT NOT NULL,
    clasificacion TEXT NOT NULL,
    duracion INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS sala (
    id_sala SERIAL PRIMARY KEY,
    id_pelicula INTEGER NOT NULL,
    nombre_sala TEXT NOT NULL,
    capacidad INTEGER NOT NULL,
    asientos_disponibles INTEGER NOT NULL,
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula),
    CONSTRAINT chk_sala_capacidad_positiva CHECK (capacidad > 0),
    CONSTRAINT chk_sala_asientos_disponibles CHECK (
        asientos_disponibles >= 0 AND asientos_disponibles <= capacidad
    )
);

CREATE TABLE IF NOT EXISTS funcion (
    id_funcion SERIAL PRIMARY KEY,
    id_pelicula INTEGER NOT NULL,
    id_sala INTEGER NOT NULL,
    fecha_funcion DATE NOT NULL,
    hora TIME NOT NULL,
    precio NUMERIC(8,2) NOT NULL,
    FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula),
    FOREIGN KEY (id_sala) REFERENCES sala(id_sala)
);

CREATE TABLE IF NOT EXISTS venta (
    id_venta SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    fecha_compra TIMESTAMP NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS detalle_venta (
    id_detalle SERIAL PRIMARY KEY,
    id_venta INTEGER NOT NULL,
    id_funcion INTEGER NOT NULL,
    asiento TEXT NOT NULL,
    codigo_boleto TEXT NOT NULL,
    CONSTRAINT uq_detalle_venta_codigo_boleto UNIQUE (codigo_boleto),
    CONSTRAINT uq_detalle_venta_funcion_asiento UNIQUE (id_funcion, asiento),
    FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
    FOREIGN KEY (id_funcion) REFERENCES funcion(id_funcion)
);
