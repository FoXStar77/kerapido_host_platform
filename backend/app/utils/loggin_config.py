import sys
from loguru import logger
from ..config import settings

def setup_logging():
    """
    Configura el logging de la aplicación.
    Remueve el handler por defecto y añade uno nuevo con un formato estructurado.
    """
    logger.remove()
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    logger.info("Logging configuration complete.")

# Se puede importar y usar el logger en cualquier parte del código
# Ejemplo:
# from ..utils.logging_config import logger
# logger.info("Mensaje de log")
