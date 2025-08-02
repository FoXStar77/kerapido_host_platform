from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import auth, users, solicitudes, conductores, vehiculos, asignaciones, pagos, emergencias, catalogos
from .middleware.rate_limiter import RateLimiterMiddleware
from .utils.logging_config import setup_logging
from .exceptions import APIException
from .config import settings

# Setup logging
setup_logging()

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KE RÁPIDO Backend API",
    description="API para la plataforma de transporte integral KE RÁPIDO",
    version="0.1.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Orígenes permitidos desde las variables de entorno
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Rate Limiter
app.add_middleware(RateLimiterMiddleware)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """
    Manejador global de excepciones para APIException.
    Devuelve un JSON con el mensaje de error y el código de estado.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Incluye todos los enrutadores de la aplicación
app.include_router(auth.router, tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(solicitudes.router, prefix="/api/v1", tags=["Solicitudes"])
app.include_router(conductores.router, prefix="/api/v1", tags=["Conductores"])
app.include_router(vehiculos.router, prefix="/api/v1", tags=["Vehículos"])
app.include_router(asignaciones.router, prefix="/api/v1", tags=["Asignaciones"])
app.include_router(pagos.router, prefix="/api/v1", tags=["Pagos"])
app.include_router(emergencias.router, prefix="/api/v1", tags=["Emergencias"])
app.include_router(catalogos.router, prefix="/api/v1", tags=["Catálogos"])

@app.get("/")
async def root():
    return {"message": "Welcome to KE RÁPIDO Backend API"}
