from fastapi import HTTPException, status

class APIException(HTTPException):
    """Clase base para todas las excepciones de la API."""
    def __init__(self, status_code: int, detail: str = "Error interno del servidor"):
        super().__init__(status_code=status_code, detail=detail)

class UnauthorizedException(APIException):
    def __init__(self, detail: str = "Credenciales inválidas"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )

class ForbiddenException(APIException):
    def __init__(self, detail: str = "No tienes permiso para realizar esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )

class NotFoundException(APIException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

class ConflictException(APIException):
    def __init__(self, detail: str = "El recurso ya existe"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )
