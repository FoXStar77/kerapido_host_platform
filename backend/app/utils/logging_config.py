# app/utils/loggin_config.py

import sys
from loguru import logger
from app.config import settings  # ← import corregido

def setup_logging():
    """
    Configura el logging de la aplicación con Loguru.
    """
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    logger.info("Logging configurado correctamente.")


# Ejemplo de uso en otro módulo:
# from app.utils.loggin_config import logger
# logger.info("Esto es un mensaje informativo.")
