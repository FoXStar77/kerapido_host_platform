from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List


class Token(BaseModel):
    """
    Esquema para la respuesta del token JWT.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Esquema para la data del token JWT.
    """

    username: Optional[str] = None


class UsuarioBase(BaseModel):
    """
    Esquema base para un usuario.
    """

    nombre: str
    apellidos: Optional[str] = None
    email: EmailStr
    telefono: Optional[str] = None
    es_conductor: bool = False
    es_cliente: bool = False
    es_admin: bool = False
    carnet_identidad: Optional[str] = None
    domicilio_actual: Optional[str] = None
    codigo_postal: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    """
    Esquema para la creación de un usuario.
    """

    password: str


class UsuarioUpdate(UsuarioBase):
    """
    Esquema para la actualización de un usuario.
    """

    password: Optional[str] = None
    email_verificado: Optional[bool] = None
    telefono_confirmado: Optional[bool] = None


class UsuarioInDB(UsuarioBase):
    """
    Esquema para un usuario tal como se almacena en la DB,
    incluyendo su ID y fechas.
    """

    id_usuario: int
    email_verificado: bool
    telefono_confirmado: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True


class ClienteBase(BaseModel):
    """
    Esquema base para un cliente.
    """

    id_tipo_cliente: Optional[int] = None


class ClienteCreate(ClienteBase):
    """
    Esquema para la creación de un cliente.
    """

    id_usuario: int


class ClienteInDB(ClienteBase):
    """
    Esquema para un cliente en la DB.
    """

    id_cliente: int
    id_usuario: int
    usuario: UsuarioInDB

    class Config:
        from_attributes = True


class ConductorBase(BaseModel):
    """
    Esquema base para un conductor.
    """

    numero_licencia: str
    fecha_vencimiento_licencia: Optional[date] = None
    id_estado_conductor: Optional[int] = 1
    calificacion_promedio: Optional[float] = 0.0


class ConductorCreate(ConductorBase):
    """
    Esquema para la creación de un conductor.
    """

    id_usuario: int


class ConductorInDB(ConductorBase):
    """
    Esquema para un conductor en la DB.
    """

    id_conductor: int
    id_usuario: int
    usuario: UsuarioInDB
    vehiculos: List["VehiculoInDB"] = []
    servicios_ofrecidos: List["ConductorServicioInDB"] = []

    class Config:
        from_attributes = True


class VehiculoBase(BaseModel):
    """
    Esquema base para un vehículo.
    """

    marca: str
    modelo: str
    matricula: str
    color: Optional[str] = None
    anno: Optional[int] = None
    capacidad_pasajero: Optional[int] = None
    capacidad_carga: Optional[float] = None
    capacidad_volumen: Optional[float] = None
    id_tipo_vehiculo: int
    id_estado_vehiculo: int = 1


class VehiculoCreate(VehiculoBase):
    """
    Esquema para la creación de un vehículo.
    """

    id_conductor: int


class VehiculoInDB(VehiculoBase):
    """
    Esquema para un vehículo en la DB.
    """

    id_vehiculo: int
    id_conductor: int

    class Config:
        from_attributes = True


class SolicitudBase(BaseModel):
    """
    Esquema base para una solicitud.
    """

    origen_lat: float
    origen_lon: float
    destino_lat: Optional[float] = None
    destino_lon: Optional[float] = None
    direccion_origen: Optional[str] = None
    direccion_destino: Optional[str] = None
    comentarios: Optional[str] = None
    precio_sugerido: Optional[float] = None
    id_tipo_servicio: int
    id_estado_solicitud: int = 1


class SolicitudCreate(SolicitudBase):
    """
    Esquema para la creación de una solicitud.
    """

    id_cliente: int


class SolicitudInDB(SolicitudBase):
    """
    Esquema para una solicitud en la DB.
    """

    id_solicitud: int
    id_cliente: int
    fecha_solicitud: datetime

    class Config:
        from_attributes = True


class AsignacionBase(BaseModel):
    """
    Esquema base para una asignación.
    """

    fecha_hora_inicio_servicio: Optional[datetime] = None
    fecha_hora_fin_servicio: Optional[datetime] = None
    precio_final: Optional[float] = None


class AsignacionCreate(AsignacionBase):
    """
    Esquema para la creación de una asignación.
    """

    id_solicitud: int
    id_conductor: int
    id_vehiculo: int


class AsignacionInDB(AsignacionBase):
    """
    Esquema para una asignación en la DB.
    """

    id_asignacion: int
    id_solicitud: int
    id_conductor: int
    id_vehiculo: int
    fecha_hora_asignacion: datetime

    class Config:
        from_attributes = True


class TransaccionPagoBase(BaseModel):
    """
    Esquema base para una transacción de pago.
    """

    monto: float
    id_moneda: int
    id_tipo_metodo_pago: int
    id_canal_pago: int
    id_estado_pago: int


class TransaccionPagoCreate(TransaccionPagoBase):
    """
    Esquema para la creación de una transacción de pago.
    """

    id_asignacion: int
    id_usuario: int
    

class TransaccionPagoInDB(TransaccionPagoBase):
    """
    Esquema para una transacción de pago en la DB.
    """

    id_transaccion: int
    id_asignacion: int
    fecha_hora_pago: datetime

    class Config:
        from_attributes = True


class NotificacionBase(BaseModel):
    """
    Esquema base para una notificación.
    """

    titulo: str
    mensaje: str


class NotificacionCreate(NotificacionBase):
    """
    Esquema para la creación de una notificación.
    """

    id_usuario: int


class NotificacionInDB(NotificacionBase):
    """
    Esquema para una notificación en la DB.
    """

    id_notificacion: int
    id_usuario: int
    leida: bool
    fecha_hora: datetime

    class Config:
        from_attributes = True


class IncidenteBase(BaseModel):
    """
    Esquema base para un incidente.
    """

    descripcion: str
    ubicacion_lat: Optional[float] = None
    ubicacion_lon: Optional[float] = None
    id_tipo_incidente: int
    id_estado_incidente: int = 1


class IncidenteCreate(IncidenteBase):
    """
    Esquema para la creación de un incidente.
    """

    id_usuario: int
    id_solicitud: Optional[int] = None


class IncidenteInDB(IncidenteBase):
    """
    Esquema para un incidente en la DB.
    """

    id_incidente: int
    id_usuario: int
    fecha_hora_incidente: datetime

    class Config:
        from_attributes = True


class RutaBase(BaseModel):
    """
    Esquema base para una ruta.
    """

    nombre: str
    origen_lat: float
    origen_lon: float
    destino_lat: float
    destino_lon: float


class RutaCreate(RutaBase):
    """
    Esquema para la creación de una ruta.
    """
    pass


class RutaInDB(RutaBase):
    """
    Esquema para una ruta en la DB.
    """

    id_ruta: int

    class Config:
        from_attributes = True


class ConductorServicioBase(BaseModel):
    """
    Esquema base para la relación conductor-servicio.
    """

    fecha_habilitacion: Optional[date] = None


class ConductorServicioCreate(ConductorServicioBase):
    """
    Esquema para la creación de una relación conductor-servicio.
    """

    id_conductor: int
    id_tipo_servicio: int


class ConductorServicioInDB(ConductorServicioBase):
    """
    Esquema para la relación conductor-servicio en la DB.
    """

    id_conductor: int
    id_tipo_servicio: int

    class Config:
        from_attributes = True

IncidenteEmergenciaCreate = IncidenteCreate
IncidenteEmergenciaInDB = IncidenteInDB