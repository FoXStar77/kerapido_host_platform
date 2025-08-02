import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-that-should-be-changed")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Configuración de CORS
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:8000").split(",")
    
    # Configuración de Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 100))
    RATE_LIMIT_INTERVAL_SECONDS: int = int(os.getenv("RATE_LIMIT_INTERVAL_SECONDS", 60))


settings = Settings()
