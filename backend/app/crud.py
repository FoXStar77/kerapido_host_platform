from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash
from .exceptions import NotFoundException, ConflictException, ForbiddenException
from .utils.logging_config import logger


# --- CRUD para Usuario ---


def get_usuario(db: Session, usuario_id: int):
    """Obtiene un usuario por su ID."""
    logger.info(f"Obteniendo usuario con id: {usuario_id}")
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id_usuario == usuario_id).first()
    if not db_usuario:
        raise NotFoundException(detail=f"Usuario con id {usuario_id} no encontrado.")
    return db_usuario


def get_usuario_by_email(db: Session, email: str):
    """Obtiene un usuario por su email."""
    logger.info(f"Obteniendo usuario con email: {email}")
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de todos los usuarios."""
    logger.info(f"Obteniendo lista de usuarios, skip={skip}, limit={limit}")
    return db.query(models.Usuario).offset(skip).limit(limit).all()


def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    """Crea un nuevo usuario en la base de datos."""
    logger.info(f"Creando nuevo usuario con email: {usuario.email}")
    db_usuario = get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise ConflictException(detail="El correo electrónico ya está registrado.")
    
    hashed_password = get_password_hash(usuario.password)
    db_usuario = models.Usuario(
        email=usuario.email,
        nombre=usuario.nombre,
        apellidos=usuario.apellidos,
        telefono=usuario.telefono,
        password_hash=hashed_password,
        es_conductor=usuario.es_conductor,
        es_cliente=usuario.es_cliente,
        es_admin=usuario.es_admin,
        carnet_identidad=usuario.carnet_identidad,
        domicilio_actual=usuario.domicilio_actual,
        codigo_postal=usuario.codigo_postal,
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioUpdate):
    """Actualiza un usuario existente por su ID."""
    logger.info(f"Actualizando usuario con id: {usuario_id}")
    db_usuario = get_usuario(db, usuario_id)
    # The get_usuario function already raises NotFoundException if the user doesn't exist.
    
    for key, value in usuario.model_dump(exclude_unset=True).items():
        if key == "password":
            db_usuario.password_hash = get_password_hash(value)
        else:
            setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def delete_usuario(db: Session, usuario_id: int):
    """Elimina un usuario por su ID."""
    logger.info(f"Eliminando usuario con id: {usuario_id}")
    db_usuario = get_usuario(db, usuario_id)
    # The get_usuario function already raises NotFoundException if the user doesn't exist.
    
    db.delete(db_usuario)
    db.commit()
    return db_usuario


# --- CRUD para Cliente ---


def get_cliente(db: Session, cliente_id: int):
    """Obtiene un cliente por su ID."""
    logger.info(f"Obteniendo cliente con id: {cliente_id}")
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == cliente_id).first()
    if not db_cliente:
        raise NotFoundException(detail=f"Cliente con id {cliente_id} no encontrado.")
    return db_cliente


def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    """Crea un nuevo cliente asociado a un usuario."""
    logger.info(f"Creando nuevo cliente para el usuario {cliente.id_usuario}")
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_usuario == cliente.id_usuario).first()
    if db_cliente:
        raise ConflictException(detail=f"El usuario con id {cliente.id_usuario} ya es cliente.")

    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


# --- CRUD para Conductor ---


def get_conductor(db: Session, conductor_id: int):
    """Obtiene un conductor por su ID."""
    logger.info(f"Obteniendo conductor con id: {conductor_id}")
    db_conductor = db.query(models.Conductor).filter(models.Conductor.id_conductor == conductor_id).first()
    if not db_conductor:
        raise NotFoundException(detail=f"Conductor con id {conductor_id} no encontrado.")
    return db_conductor


def create_conductor(db: Session, conductor: schemas.ConductorCreate):
    """Crea un nuevo conductor asociado a un usuario."""
    logger.info(f"Creando nuevo conductor para el usuario {conductor.id_usuario}")
    db_conductor = db.query(models.Conductor).filter(models.Conductor.id_usuario == conductor.id_usuario).first()
    if db_conductor:
        raise ConflictException(detail=f"El usuario con id {conductor.id_usuario} ya es conductor.")
    
    db_conductor = models.Conductor(**conductor.model_dump())
    db.add(db_conductor)
    db.commit()
    db.refresh(db_conductor)
    return db_conductor


def get_conductores(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de todos los conductores."""
    logger.info(f"Obteniendo lista de conductores, skip={skip}, limit={limit}")
    return db.query(models.Conductor).offset(skip).limit(limit).all()


# --- CRUD para Vehiculo ---


def get_vehiculo(db: Session, vehiculo_id: int):
    """Obtiene un vehículo por su ID."""
    logger.info(f"Obteniendo vehículo con id: {vehiculo_id}")
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.id_vehiculo == vehiculo_id).first()
    if not db_vehiculo:
        raise NotFoundException(detail=f"Vehículo con id {vehiculo_id} no encontrado.")
    return db_vehiculo


def get_vehiculos_by_conductor(db: Session, conductor_id: int):
    """Obtiene todos los vehículos de un conductor específico."""
    logger.info(f"Obteniendo vehículos para el conductor con id: {conductor_id}")
    return db.query(models.Vehiculo).filter(models.Vehiculo.id_conductor == conductor_id).all()


def create_vehiculo(db: Session, vehiculo: schemas.VehiculoCreate):
    """Crea un nuevo vehículo para un conductor."""
    logger.info(f"Creando nuevo vehículo con placa: {vehiculo.placa}")
    db_vehiculo = db.query(models.Vehiculo).filter(models.Vehiculo.placa == vehiculo.placa).first()
    if db_vehiculo:
        raise ConflictException(detail="Ya existe un vehículo con esa placa.")
        
    db_vehiculo = models.Vehiculo(**vehiculo.model_dump())
    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)
    return db_vehiculo


# --- CRUD para Solicitud ---


def get_solicitud(db: Session, solicitud_id: int):
    """Obtiene una solicitud por su ID."""
    logger.info(f"Obteniendo solicitud con id: {solicitud_id}")
    db_solicitud = db.query(models.Solicitud).filter(models.Solicitud.id_solicitud == solicitud_id).first()
    if not db_solicitud:
        raise NotFoundException(detail=f"Solicitud con id {solicitud_id} no encontrada.")
    return db_solicitud


def get_solicitudes_by_cliente(db: Session, cliente_id: int):
    """Obtiene todas las solicitudes de un cliente específico."""
    logger.info(f"Obteniendo solicitudes para el cliente con id: {cliente_id}")
    return db.query(models.Solicitud).filter(models.Solicitud.id_cliente == cliente_id).all()


def create_solicitud(db: Session, solicitud: schemas.SolicitudCreate):
    """Crea una nueva solicitud de servicio."""
    logger.info(f"Creando nueva solicitud para el cliente {solicitud.id_cliente}")
    db_solicitud = models.Solicitud(**solicitud.model_dump())
    db.add(db_solicitud)
    db.commit()
    db.refresh(db_solicitud)
    return db_solicitud


# --- CRUD para Asignacion ---


def get_asignacion(db: Session, asignacion_id: int):
    """Obtiene una asignación por su ID."""
    logger.info(f"Obteniendo asignación con id: {asignacion_id}")
    db_asignacion = db.query(models.Asignacion).filter(models.Asignacion.id_asignacion == asignacion_id).first()
    if not db_asignacion:
        raise NotFoundException(detail=f"Asignación con id {asignacion_id} no encontrada.")
    return db_asignacion


def get_asignaciones_by_conductor(db: Session, conductor_id: int):
    """Obtiene todas las asignaciones de un conductor."""
    logger.info(f"Obteniendo asignaciones para el conductor con id: {conductor_id}")
    return db.query(models.Asignacion).filter(models.Asignacion.id_conductor == conductor_id).all()


def create_asignacion(db: Session, asignacion: schemas.AsignacionCreate):
    """Crea una nueva asignación de servicio."""
    logger.info(f"Creando nueva asignación para la solicitud {asignacion.id_solicitud}")
    db_asignacion = db.query(models.Asignacion).filter(models.Asignacion.id_solicitud == asignacion.id_solicitud).first()
    if db_asignacion:
        raise ConflictException(detail=f"La solicitud con id {asignacion.id_solicitud} ya tiene una asignación.")
        
    db_asignacion = models.Asignacion(**asignacion.model_dump())
    db.add(db_asignacion)
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


def update_asignacion_precio(db: Session, asignacion_id: int, precio_final: float):
    """Actualiza el precio final de una asignación."""
    logger.info(f"Actualizando precio final de la asignación {asignacion_id}")
    db_asignacion = get_asignacion(db, asignacion_id)
    # The get_asignacion function already raises NotFoundException if the assignment doesn't exist.
    
    db_asignacion.precio_final = precio_final
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion


# --- CRUD para TransaccionPago ---


def get_transaccion_pago(db: Session, transaccion_id: int):
    """Obtiene una transacción de pago por su ID."""
    logger.info(f"Obteniendo transacción de pago con id: {transaccion_id}")
    db_transaccion = db.query(models.TransaccionPago).filter(models.TransaccionPago.id_transaccion == transaccion_id).first()
    if not db_transaccion:
        raise NotFoundException(detail=f"Transacción de pago con id {transaccion_id} no encontrada.")
    return db_transaccion


def create_transaccion_pago(db: Session, pago: schemas.TransaccionPagoCreate):
    """Crea una nueva transacción de pago."""
    logger.info(f"Creando nueva transacción de pago para el usuario {pago.id_usuario}")
    db_pago = models.TransaccionPago(**pago.model_dump())
    db.add(db_pago)
    db.commit()
    db.refresh(db_pago)
    return db_pago


# --- CRUD para Notificacion ---


def get_notificaciones_by_user(db: Session, usuario_id: int):
    """Obtiene todas las notificaciones de un usuario."""
    logger.info(f"Obteniendo notificaciones para el usuario con id: {usuario_id}")
    return db.query(models.Notificacion).filter(models.Notificacion.id_usuario == usuario_id).all()


def create_notificacion(db: Session, notificacion: schemas.NotificacionCreate):
    """Crea una nueva notificación para un usuario."""
    logger.info(f"Creando nueva notificación para el usuario {notificacion.id_usuario}")
    db_notificacion = models.Notificacion(**notificacion.model_dump())
    db.add(db_notificacion)
    db.commit()
    db.refresh(db_notificacion)
    return db_notificacion


# --- CRUD para Incidente ---


def get_incidente(db: Session, incidente_id: int):
    """Obtiene un incidente por su ID."""
    logger.info(f"Obteniendo incidente con id: {incidente_id}")
    db_incidente = db.query(models.Incidente).filter(models.Incidente.id_incidente == incidente_id).first()
    if not db_incidente:
        raise NotFoundException(detail=f"Incidente con id {incidente_id} no encontrado.")
    return db_incidente


def create_incidente(db: Session, incidente: schemas.IncidenteCreate):
    """Crea un nuevo incidente."""
    logger.info(f"Creando nuevo incidente para el usuario {incidente.id_usuario}")
    db_incidente = models.Incidente(**incidente.model_dump())
    db.add(db_incidente)
    db.commit()
    db.refresh(db_incidente)
    return db_incidente


# --- CRUD para Ruta ---


def get_ruta(db: Session, ruta_id: int):
    """Obtiene una ruta por su ID."""
    logger.info(f"Obteniendo ruta con id: {ruta_id}")
    db_ruta = db.query(models.Ruta).filter(models.Ruta.id_ruta == ruta_id).first()
    if not db_ruta:
        raise NotFoundException(detail=f"Ruta con id {ruta_id} no encontrada.")
    return db_ruta


def get_rutas(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene todas las rutas disponibles."""
    logger.info(f"Obteniendo rutas, skip={skip}, limit={limit}")
    return db.query(models.Ruta).offset(skip).limit(limit).all()


def create_ruta(db: Session, ruta: schemas.RutaCreate):
    """Crea una nueva ruta."""
    logger.info(f"Creando nueva ruta con origen: {ruta.origen} y destino: {ruta.destino}")
    db_ruta = models.Ruta(**ruta.model_dump())
    db.add(db_ruta)
    db.commit()
    db.refresh(db_ruta)
    return db_ruta


# --- CRUD para ConductorServicio ---


def create_conductor_servicio(db: Session, servicio: schemas.ConductorServicioCreate):
    """Asocia un servicio a un conductor."""
    logger.info(f"Asociando servicio {servicio.id_tipo_servicio} al conductor {servicio.id_conductor}")
    db_servicio = db.query(models.ConductorServicio).filter(
        models.ConductorServicio.id_conductor == servicio.id_conductor,
        models.ConductorServicio.id_tipo_servicio == servicio.id_tipo_servicio
    ).first()
    if db_servicio:
        raise ConflictException(detail="Este servicio ya está asociado a este conductor.")
    
    db_servicio = models.ConductorServicio(**servicio.model_dump())
    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)
    return db_servicio


def get_servicios_by_conductor(db: Session, conductor_id: int):
    """Obtiene los servicios ofrecidos por un conductor."""
    logger.info(f"Obteniendo servicios para el conductor con id: {conductor_id}")
    return db.query(models.ConductorServicio).filter(models.ConductorServicio.id_conductor == conductor_id).all()


# --- CRUD para tablas de catálogo ---


def get_tipos_cliente(db: Session):
    """Obtiene todos los tipos de cliente."""
    logger.info("Obteniendo todos los tipos de cliente.")
    return db.query(models.TipoCliente).all()


def get_estados_conductor(db: Session):
    """Obtiene todos los estados de conductor."""
    logger.info("Obteniendo todos los estados de conductor.")
    return db.query(models.EstadoConductor).all()


def get_tipos_vehiculo(db: Session):
    """Obtiene todos los tipos de vehículo."""
    logger.info("Obteniendo todos los tipos de vehículo.")
    return db.query(models.TipoVehiculo).all()


def get_estados_vehiculo(db: Session):
    """Obtiene todos los estados de vehículo."""
    logger.info("Obteniendo todos los estados de vehículo.")
    return db.query(models.EstadoVehiculo).all()


def get_tipos_servicio(db: Session):
    """Obtiene todos los tipos de servicio."""
    logger.info("Obteniendo todos los tipos de servicio.")
    return db.query(models.TipoServicio).all()


def get_estados_solicitud(db: Session):
    """Obtiene todos los estados de solicitud."""
    logger.info("Obteniendo todos los estados de solicitud.")
    return db.query(models.EstadoSolicitud).all()


def get_all_tipos_carga(db: Session):
    """Obtiene todos los tipos de carga."""
    logger.info("Obteniendo todos los tipos de carga.")
    return db.query(models.TipoCarga).all()


def get_all_tipos_incidente(db: Session):
    """Obtiene todos los tipos de incidente."""
    logger.info("Obteniendo todos los tipos de incidente.")
    return db.query(models.TipoIncidente).all()


def get_all_estados_incidente(db: Session):
    """Obtiene todos los estados de incidente."""
    logger.info("Obteniendo todos los estados de incidente.")
    return db.query(models.EstadoIncidente).all()


def get_all_estados_reserva(db: Session):
    """Obtiene todos los estados de reserva."""
    logger.info("Obteniendo todos los estados de reserva.")
    return db.query(models.EstadoReserva).all()


def get_all_monedas(db: Session):
    """Obtiene todas las monedas."""
    logger.info("Obteniendo todas las monedas.")
    return db.query(models.Moneda).all()


def get_all_tipos_metodo_pago(db: Session):
    """Obtiene todos los tipos de método de pago."""
    logger.info("Obteniendo todos los tipos de método de pago.")
    return db.query(models.TipoMetodoPago).all()


def get_all_canales_pago(db: Session):
    """Obtiene todos los canales de pago."""
    logger.info("Obteniendo todos los canales de pago.")
    return db.query(models.CanalPago).all()


def get_all_estados_pago(db: Session):
    """Obtiene todos los estados de pago."""
    logger.info("Obteniendo todos los estados de pago.")
    return db.query(models.EstadoPago).all()


def get_all_tipos_tarifa(db: Session):
    """Obtiene todos los tipos de tarifa."""
    logger.info("Obteniendo todos los tipos de tarifa.")
    return db.query(models.TipoTarifa).all()


def get_all_tarifas(db: Session):
    """Obtiene todas las tarifas."""
    logger.info("Obteniendo todas las tarifas.")
    return db.query(models.Tarifa).all()
