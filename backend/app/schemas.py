from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UsuarioBase(BaseModel):
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
    password: str


class UsuarioUpdate(UsuarioBase):
    password: Optional[str] = None
    email_verificado: Optional[bool] = None
    telefono_confirmado: Optional[bool] = None


class UsuarioInDB(UsuarioBase):
    id_usuario: int
    email_verificado: bool
    telefono_confirmado: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True


class ClienteBase(BaseModel):
    id_tipo_cliente: Optional[int] = None


class ClienteCreate(ClienteBase):
    id_usuario: int


class ClienteInDB(ClienteBase):
    id_cliente: int
    id_usuario: int
    usuario: UsuarioInDB

    class Config:
        from_attributes = True


class ConductorBase(BaseModel):
    numero_licencia: str
    fecha_vencimiento_licencia: Optional[date] = None
    id_estado_conductor: Optional[int] = 1
    calificacion_promedio: Optional[float] = 0.0


class ConductorCreate(ConductorBase):
    id_usuario: int


class ConductorInDB(ConductorBase):
    id_conductor: int
    id_usuario: int
    usuario: UsuarioInDB
    vehiculos: List["VehiculoInDB"] = []
    servicios_ofrecidos: List["ConductorServicioInDB"] = []

    class Config:
        from_attributes = True


class VehiculoBase(BaseModel):
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
    id_conductor: int


class VehiculoInDB(VehiculoBase):
    id_vehiculo: int
    id_conductor: int

    class Config:
        from_attributes = True


class SolicitudBase(BaseModel):
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
    id_cliente: int


class SolicitudInDB(SolicitudBase):
    id_solicitud: int
    id_cliente: int
    fecha_solicitud: datetime

    class Config:
        from_attributes = True


class AsignacionBase(BaseModel):
    fecha_hora_inicio_servicio: Optional[datetime] = None
    fecha_hora_fin_servicio: Optional[datetime] = None
    precio_final: Optional[float] = None


class AsignacionCreate(AsignacionBase):
    id_solicitud: int
    id_conductor: int
    id_vehiculo: int


class AsignacionInDB(AsignacionBase):
    id_asignacion: int
    id_solicitud: int
    id_conductor: int
    id_vehiculo: int
    fecha_hora_asignacion: datetime

    class Config:
        from_attributes = True


class TransaccionPagoBase(BaseModel):
    monto: float
    id_moneda: int
    id_tipo_metodo_pago: int
    id_canal_pago: int
    id_estado_pago: int


class TransaccionPagoCreate(TransaccionPagoBase):
    id_asignacion: int
    id_usuario: int


class TransaccionPagoInDB(TransaccionPagoBase):
    id_transaccion: int
    id_asignacion: int
    fecha_hora_pago: datetime

    class Config:
        from_attributes = True


class NotificacionBase(BaseModel):
    titulo: str
    mensaje: str


class NotificacionCreate(NotificacionBase):
    id_usuario: int


class NotificacionInDB(NotificacionBase):
    id_notificacion: int
    id_usuario: int
    leida: bool
    fecha_hora: datetime

    class Config:
        from_attributes = True


class IncidenteBase(BaseModel):
    descripcion: str
    ubicacion_lat: Optional[float] = None
    ubicacion_lon: Optional[float] = None
    id_tipo_incidente: int
    id_estado_incidente: int = 1


class IncidenteCreate(IncidenteBase):
    id_usuario: int
    id_solicitud: Optional[int] = None


class IncidenteInDB(IncidenteBase):
    id_incidente: int
    id_usuario: int
    fecha_hora_incidente: datetime

    class Config:
        from_attributes = True


class RutaBase(BaseModel):
    nombre: str
    origen_lat: float
    origen_lon: float
    destino_lat: float
    destino_lon: float


class RutaCreate(RutaBase):
    pass


class RutaInDB(RutaBase):
    id_ruta: int

    class Config:
        from_attributes = True


class ConductorServicioBase(BaseModel):
    fecha_habilitacion: Optional[date] = None


class ConductorServicioCreate(ConductorServicioBase):
    id_conductor: int
    id_tipo_servicio: int


class ConductorServicioInDB(ConductorServicioBase):
    id_conductor: int
    id_tipo_servicio: int

    class Config:
        from_attributes = True


# Catálogos

class TipoClienteSchema(BaseModel):
    id_tipo_cliente: int
    nombre: str

    class Config:
        from_attributes = True


class EstadoConductorSchema(BaseModel):
    id_estado_conductor: int
    descripcion: str

    class Config:
        from_attributes = True


class TipoVehiculoSchema(BaseModel):
    id_tipo_vehiculo: int
    descripcion: str

    class Config:
        from_attributes = True


class EstadoVehiculoSchema(BaseModel):
    id_estado_vehiculo: int
    descripcion: str

    class Config:
        from_attributes = True


class TipoServicioSchema(BaseModel):
    id_tipo_servicio: int
    descripcion: str

    class Config:
        from_attributes = True


class EstadoSolicitudSchema(BaseModel):
    id_estado_solicitud: int
    descripcion: str

    class Config:
        from_attributes = True


IncidenteEmergenciaCreate = IncidenteCreate
IncidenteEmergenciaInDB = IncidenteInDB
