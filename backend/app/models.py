from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Usuario(Base):
    """
    Modelo de la tabla de usuarios.
    Representa a todos los usuarios de la plataforma (clientes, conductores, administradores).
    """

    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellidos = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    es_conductor = Column(Boolean, default=False, nullable=False)
    es_cliente = Column(Boolean, default=False, nullable=False)
    es_admin = Column(Boolean, default=False, nullable=False)
    carnet_identidad = Column(String, unique=True)
    domicilio_actual = Column(String)
    codigo_postal = Column(String)
    email_verificado = Column(Boolean, default=False, nullable=False)
    telefono_confirmado = Column(Boolean, default=False, nullable=False)
    fecha_registro = Column(DateTime, default=func.now())

    cliente = relationship("Cliente", back_populates="usuario", uselist=False)
    conductor = relationship("Conductor", back_populates="usuario", uselist=False)


class Cliente(Base):
    """
    Modelo de la tabla de clientes.
    """

    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    id_tipo_cliente = Column(Integer, ForeignKey("tipos_cliente.id_tipo_cliente"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True)

    usuario = relationship("Usuario", back_populates="cliente")
    tipo_cliente = relationship("TipoCliente")


class Conductor(Base):
    """
    Modelo de la tabla de conductores.
    """

    __tablename__ = "conductores"

    id_conductor = Column(Integer, primary_key=True, index=True)
    numero_licencia = Column(String, unique=True, nullable=False)
    fecha_vencimiento_licencia = Column(Date)
    calificacion_promedio = Column(Float, default=0.0)
    id_estado_conductor = Column(
        Integer, ForeignKey("estados_conductor.id_estado_conductor")
    )
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), unique=True)

    usuario = relationship("Usuario", back_populates="conductor")
    estado = relationship("EstadoConductor")
    vehiculos = relationship("Vehiculo", back_populates="conductor")
    servicios_ofrecidos = relationship(
        "ConductorServicio", back_populates="conductor"
    )


class Vehiculo(Base):
    """
    Modelo de la tabla de vehículos.
    """

    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    color = Column(String)
    anno = Column(Integer)
    capacidad_pasajero = Column(Integer)
    capacidad_carga = Column(Float)
    capacidad_volumen = Column(Float)
    id_tipo_vehiculo = Column(Integer, ForeignKey("tipos_vehiculo.id_tipo_vehiculo"))
    id_estado_vehiculo = Column(
        Integer, ForeignKey("estados_vehiculo.id_estado_vehiculo")
    )
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"))

    tipo_vehiculo = relationship("TipoVehiculo")
    estado = relationship("EstadoVehiculo")
    conductor = relationship("Conductor", back_populates="vehiculos")


class Solicitud(Base):
    """
    Modelo de la tabla de solicitudes de servicio.
    """

    __tablename__ = "solicitudes"

    id_solicitud = Column(Integer, primary_key=True, index=True)
    origen_lat = Column(Float, nullable=False)
    origen_lon = Column(Float, nullable=False)
    destino_lat = Column(Float)
    destino_lon = Column(Float)
    direccion_origen = Column(String)
    direccion_destino = Column(String)
    comentarios = Column(Text)
    precio_sugerido = Column(Float)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    id_tipo_servicio = Column(Integer, ForeignKey("tipos_servicio.id_tipo_servicio"))
    id_estado_solicitud = Column(
        Integer, ForeignKey("estados_solicitud.id_estado_solicitud")
    )
    fecha_solicitud = Column(DateTime, default=func.now())

    cliente = relationship("Cliente")
    tipo_servicio = relationship("TipoServicio")
    estado = relationship("EstadoSolicitud")


class Asignacion(Base):
    """
    Modelo de la tabla de asignaciones de servicio.
    """

    __tablename__ = "asignaciones"

    id_asignacion = Column(Integer, primary_key=True, index=True)
    fecha_hora_asignacion = Column(DateTime, default=func.now(), nullable=False)
    fecha_hora_inicio_servicio = Column(DateTime)
    fecha_hora_fin_servicio = Column(DateTime)
    precio_final = Column(Float)
    id_solicitud = Column(Integer, ForeignKey("solicitudes.id_solicitud"), unique=True)
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"))
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))

    solicitud = relationship("Solicitud")
    conductor = relationship("Conductor")
    vehiculo = relationship("Vehiculo")
    pago = relationship("TransaccionPago", back_populates="asignacion", uselist=False)


class TransaccionPago(Base):
    """
    Modelo de la tabla de transacciones de pago.
    """

    __tablename__ = "transacciones_pago"

    id_transaccion = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    fecha_hora_pago = Column(DateTime, default=func.now())
    id_asignacion = Column(
        Integer, ForeignKey("asignaciones.id_asignacion"), unique=True
    )
    id_moneda = Column(Integer, ForeignKey("monedas.id_moneda"))
    id_tipo_metodo_pago = Column(
        Integer, ForeignKey("tipos_metodo_pago.id_tipo_metodo_pago")
    )
    id_canal_pago = Column(Integer, ForeignKey("canales_pago.id_canal_pago"))
    id_estado_pago = Column(Integer, ForeignKey("estados_pago.id_estado_pago"))

    asignacion = relationship("Asignacion", back_populates="pago")
    moneda = relationship("Moneda")
    tipo_metodo_pago = relationship("TipoMetodoPago")
    canal_pago = relationship("CanalPago")
    estado_pago = relationship("EstadoPago")


class Notificacion(Base):
    """
    Modelo de la tabla de notificaciones.
    """

    __tablename__ = "notificaciones"

    id_notificacion = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    mensaje = Column(Text, nullable=False)
    leida = Column(Boolean, default=False)
    fecha_hora = Column(DateTime, default=func.now())
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))

    usuario = relationship("Usuario")


class Incidente(Base):
    """
    Modelo de la tabla de incidentes.
    """

    __tablename__ = "incidentes"

    id_incidente = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    fecha_hora_incidente = Column(DateTime, default=func.now())
    ubicacion_lat = Column(Float)
    ubicacion_lon = Column(Float)
    id_tipo_incidente = Column(
        Integer, ForeignKey("tipos_incidente.id_tipo_incidente")
    )
    id_estado_incidente = Column(
        Integer, ForeignKey("estados_incidente.id_estado_incidente")
    )
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    id_solicitud = Column(
        Integer, ForeignKey("solicitudes.id_solicitud"), nullable=True
    )

    tipo_incidente = relationship("TipoIncidente")
    estado_incidente = relationship("EstadoIncidente")
    usuario = relationship("Usuario")
    solicitud = relationship("Solicitud")


class Ruta(Base):
    """
    Modelo de la tabla de rutas.
    """

    __tablename__ = "rutas"
    id_ruta = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    origen_lat = Column(Float, nullable=False)
    origen_lon = Column(Float, nullable=False)
    destino_lat = Column(Float, nullable=False)
    destino_lon = Column(Float, nullable=False)


# --- TABLAS DE CATÁLOGO / LOOKUP TABLES ---


class TipoCliente(Base):
    """
    Modelo de la tabla de tipos de cliente.
    """

    __tablename__ = "tipos_cliente"
    id_tipo_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class EstadoConductor(Base):
    """
    Modelo de la tabla de estados de conductor.
    """

    __tablename__ = "estados_conductor"
    id_estado_conductor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class TipoVehiculo(Base):
    """
    Modelo de la tabla de tipos de vehículo.
    """

    __tablename__ = "tipos_vehiculo"
    id_tipo_vehiculo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    capacidad_maxima_pasajero = Column(Integer)
    capacidad_maxima_carga = Column(Float)
    capacidad_maxima_volumen = Column(Float)


class EstadoVehiculo(Base):
    """
    Modelo de la tabla de estados de vehículo.
    """

    __tablename__ = "estados_vehiculo"
    id_estado_vehiculo = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class TipoServicio(Base):
    """
    Modelo de la tabla de tipos de servicio.
    """

    __tablename__ = "tipos_servicio"
    id_tipo_servicio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String)
    es_colectivo = Column(Boolean, default=False, nullable=False)


class EstadoSolicitud(Base):
    """
    Modelo de la tabla de estados de solicitud.
    """

    __tablename__ = "estados_solicitud"
    id_estado_solicitud = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class TipoCarga(Base):
    """
    Modelo de la tabla de tipos de carga.
    """

    __tablename__ = "tipos_carga"
    id_tipo_carga = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String)


class TipoIncidente(Base):
    """
    Modelo de la tabla de tipos de incidente.
    """

    __tablename__ = "tipos_incidente"
    id_tipo_incidente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class EstadoIncidente(Base):
    """
    Modelo de la tabla de estados de incidente.
    """

    __tablename__ = "estados_incidente"
    id_estado_incidente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class EstadoReserva(Base):
    """
    Modelo de la tabla de estados de reserva.
    """

    __tablename__ = "estados_reserva"
    id_estado_reserva = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class Moneda(Base):
    """
    Modelo de la tabla de monedas.
    """

    __tablename__ = "monedas"
    id_moneda = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, unique=True, nullable=False)


class TipoMetodoPago(Base):
    """
    Modelo de la tabla de tipos de método de pago.
    """

    __tablename__ = "tipos_metodo_pago"
    id_tipo_metodo_pago = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class CanalPago(Base):
    """
    Modelo de la tabla de canales de pago.
    """

    __tablename__ = "canales_pago"
    id_canal_pago = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)


class EstadoPago(Base):
    """
    Modelo de la tabla de estados de pago.
    """

    __tablename__ = "estados_pago"
    id_estado_pago = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)


class TipoTarifa(Base):
    """
    Modelo de la tabla de tipos de tarifa.
    """

    __tablename__ = "tipos_tarifa"
    id_tipo_tarifa = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)


class Tarifa(Base):
    """
    Modelo de la tabla de tarifas.
    """

    __tablename__ = "tarifas"
    id_tarifa = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    fecha_vigencia = Column(Date, nullable=False)
    es_fija = Column(Boolean, default=False)
    id_moneda = Column(Integer, ForeignKey("monedas.id_moneda"))
    id_tipo_tarifa = Column(Integer, ForeignKey("tipos_tarifa.id_tipo_tarifa"))

    moneda = relationship("Moneda")
    tipo_tarifa = relationship("TipoTarifa")


class ConductorServicio(Base):
    """
    Modelo de la tabla de relación entre conductores y servicios.
    """

    __tablename__ = "conductor_servicio"
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"), primary_key=True)
    id_tipo_servicio = Column(Integer, ForeignKey("tipos_servicio.id_tipo_servicio"), primary_key=True)
    fecha_habilitacion = Column(Date)

    conductor = relationship("Conductor", back_populates="servicios_ofrecidos")
    tipo_servicio = relationship("TipoServicio")
