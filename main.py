from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.base_datos import inicializar
from routers import detalles_venta, funciones, peliculas, registros, salas, usuarios, ventas

app = FastAPI(
    title="Sistema de Gestion de Cine Cinemax",
    version="1.0",
    description="API REST para gestion de usuarios, peliculas, salas, funciones, ventas y boletos",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

inicializar()

app.include_router(usuarios.router)
app.include_router(peliculas.router)
app.include_router(salas.router)
app.include_router(funciones.router)
app.include_router(ventas.router)
app.include_router(detalles_venta.router)
app.include_router(registros.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema de Gestion de Cine Cinemax",
        "version": "1.0",
        "docs": "/docs",
    }
