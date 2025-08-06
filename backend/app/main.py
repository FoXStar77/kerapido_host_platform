# app/main.py

from fastapi import FastAPI
from app.utils.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from app.routers import registro


from app.routers import (
    auth,
    users,
    catalogos,
    conductores,
    vehiculos,
    solicitudes,
    asignaciones,
    pagos,
    emergencias,
)
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.utils.logging_config import setup_logging
from app.config import settings


# Inicializa el sistema de logs
setup_logging()

app = FastAPI(
    title="KE RÁPIDO",
    description="API ligera para servicios de transporte urbano",
    version="1.0.0",
)

# CORS Middleware (importantísimo para frontend)
app.include_router(registro.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o restringe según dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Rate Limiting (debe ir antes de los routers)
app.add_middleware(RateLimiterMiddleware)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(catalogos.router)
app.include_router(conductores.router)
app.include_router(vehiculos.router)
app.include_router(solicitudes.router)
app.include_router(asignaciones.router)
app.include_router(pagos.router)
app.include_router(emergencias.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "KE RÁPIDO API activa"}
