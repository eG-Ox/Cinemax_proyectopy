import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "cine"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        cursor_factory=RealDictCursor,
    )


@contextmanager
def conexion_bd():
    conn = obtener_conexion()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def inicializar():
    with conexion_bd() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario(
                id_usuario SERIAL PRIMARY KEY,
                nombres_usuario TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pelicula(
                id_pelicula SERIAL PRIMARY KEY,
                titulo TEXT NOT NULL,
                genero TEXT NOT NULL,
                clasificacion TEXT NOT NULL,
                duracion INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sala(
                id_sala SERIAL PRIMARY KEY,
                nombre_sala TEXT NOT NULL,
                capacidad INTEGER NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS funcion(
                id_funcion SERIAL PRIMARY KEY,
                id_pelicula INTEGER NOT NULL,
                id_sala INTEGER NOT NULL,
                fecha_funcion DATE NOT NULL,
                hora TIME NOT NULL,
                precio NUMERIC(8,2) NOT NULL,
                FOREIGN KEY (id_pelicula) REFERENCES pelicula(id_pelicula),
                FOREIGN KEY (id_sala) REFERENCES sala(id_sala)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS venta(
                id_venta SERIAL PRIMARY KEY,
                id_usuario INTEGER NOT NULL,
                fecha_compra TIMESTAMP NOT NULL,
                FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_venta(
                id_detalle SERIAL PRIMARY KEY,
                id_venta INTEGER NOT NULL,
                id_funcion INTEGER NOT NULL,
                asiento TEXT NOT NULL,
                codigo_boleto TEXT NOT NULL,
                CONSTRAINT uq_detalle_venta_codigo_boleto UNIQUE (codigo_boleto),
                CONSTRAINT uq_detalle_venta_funcion_asiento UNIQUE (id_funcion, asiento),
                FOREIGN KEY (id_venta) REFERENCES venta(id_venta),
                FOREIGN KEY (id_funcion) REFERENCES funcion(id_funcion)
            )
        """)

        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = 'uq_detalle_venta_funcion_asiento'
                ) THEN
                    ALTER TABLE detalle_venta
                    ADD CONSTRAINT uq_detalle_venta_funcion_asiento
                    UNIQUE (id_funcion, asiento);
                END IF;
            END $$;
        """)

        conn.commit()
