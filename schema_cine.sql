CREATE DATABASE cine;
USE cine;

-- ===========================
-- TABLA USUARIO
-- ===========================
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombres_usuario VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE
);

-- ===========================
-- TABLA PELICULA
-- ===========================
CREATE TABLE pelicula (
    id_pelicula INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    genero VARCHAR(50) NOT NULL,
    clasificacion VARCHAR(20) NOT NULL,
    duracion INT NOT NULL
);

-- ===========================
-- TABLA SALA
-- ===========================
CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL
);

-- ===========================
-- TABLA FUNCION
-- ===========================
CREATE TABLE funcion (
    id_funcion INT AUTO_INCREMENT PRIMARY KEY,
    id_pelicula INT NOT NULL,
    id_sala INT NOT NULL,
    fecha_funcion DATE NOT NULL,
    hora TIME NOT NULL,
    precio DECIMAL(8,2) NOT NULL,

    CONSTRAINT fk_funcion_pelicula
        FOREIGN KEY (id_pelicula)
        REFERENCES pelicula(id_pelicula),

    CONSTRAINT fk_funcion_sala
        FOREIGN KEY (id_sala)
        REFERENCES sala(id_sala)
);

-- ===========================
-- TABLA VENTA
-- ===========================
CREATE TABLE venta (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    fecha_compra DATETIME NOT NULL,

    CONSTRAINT fk_venta_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
);

-- ===========================
-- TABLA DETALLE_VENTA
-- ===========================
CREATE TABLE detalle_venta (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_funcion INT NOT NULL,
    asiento VARCHAR(10) NOT NULL,
    codigo_boleto VARCHAR(50) NOT NULL UNIQUE,

    CONSTRAINT fk_detalle_venta
        FOREIGN KEY (id_venta)
        REFERENCES venta(id_venta),

    CONSTRAINT fk_detalle_funcion
        FOREIGN KEY (id_funcion)
        REFERENCES funcion(id_funcion)
);
