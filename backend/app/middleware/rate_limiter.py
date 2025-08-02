# app/middleware/rate_limiter.py

import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from collections import defaultdict

from app.config import settings  # ← import corregido

# Este diccionario almacena peticiones por IP.
# ¡No usar en producción real! No es persistente ni distribuido.
request_counts = defaultdict(lambda: {"count": 0, "last_reset": time.time()})


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Reinicia contador si se supera el intervalo
        if current_time - request_counts[client_ip]["last_reset"] > settings.RATE_LIMIT_INTERVAL_SECONDS:
            request_counts[client_ip]["count"] = 0
            request_counts[client_ip]["last_reset"] = current_time

        # Incrementa y verifica límite
        request_counts[client_ip]["count"] += 1
        if request_counts[client_ip]["count"] > settings.RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Demasiadas peticiones. Intente más tarde."
            )

        response = await call_next(request)
        return response
