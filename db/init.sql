-- ******************************************************************************
-- TABLAS DE CATÁLOGO / LOOKUP TABLES
-- ******************************************************************************

CREATE TABLE tipos_cliente (
    id_tipo_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE estados_conductor (
    id_estado_conductor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE tipos_vehiculo (
    id_tipo_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    capacidad_maxima_pasajero INTEGER,
    capacidad_maxima_carga REAL,
    capacidad_maxima_volumen REAL
);

CREATE TABLE estados_vehiculo (
    id_estado_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE tipos_servicio (
    id_tipo_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT,
    es_colectivo BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE estados_solicitud (
    id_estado_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE tipos_carga (
    id_tipo_carga INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE tipos_incidente (
    id_tipo_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE estados_incidente (
    id_estado_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE estados_reserva (
    id_estado_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE monedas (
    id_moneda INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL
);

CREATE TABLE tipos_metodo_pago (
    id_tipo_metodo_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE canales_pago (
    id_canal_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);

CREATE TABLE estados_pago (
    id_estado_pago INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE tipos_tarifa (
    id_tipo_tarifa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);

-- ******************************************************************************
-- TABLAS PRINCIPALES DEL NEGOCIO
-- ******************************************************************************

CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellidos TEXT,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    es_conductor BOOLEAN DEFAULT FALSE NOT NULL,
    es_cliente BOOLEAN DEFAULT FALSE NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE NOT NULL,
    carnet_identidad TEXT UNIQUE,
    domicilio_actual TEXT,
    codigo_postal TEXT,
    email_verificado BOOLEAN DEFAULT FALSE NOT NULL,
    telefono_confirmado BOOLEAN DEFAULT FALSE NOT NULL,
    fecha_registro DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tipo_cliente INTEGER,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_tipo_cliente) REFERENCES tipos_cliente(id_tipo_cliente),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE conductores (
    id_conductor INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_licencia TEXT UNIQUE NOT NULL,
    fecha_vencimiento_licencia DATE,
    id_estado_conductor INTEGER NOT NULL DEFAULT 1,
    calificacion_promedio REAL DEFAULT 0.0,
    id_usuario INTEGER NOT NULL,
    FOREIGN KEY (id_estado_conductor) REFERENCES estados_conductor(id_estado_conductor),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE vehiculos (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    marca TEXT,
    modelo TEXT,
    ano INTEGER,
    id_estado_vehiculo INTEGER NOT NULL DEFAULT 1,
    id_tipo_vehiculo INTEGER NOT NULL,
    id_conductor INTEGER,
    FOREIGN KEY (id_estado_vehiculo) REFERENCES estados_vehiculo(id_estado_vehiculo),
    FOREIGN KEY (id_tipo_vehiculo) REFERENCES tipos_vehiculo(id_tipo_vehiculo),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_conductor)
);

CREATE TABLE rutas (
    id_ruta INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_ruta TEXT,
    origen_ruta_texto TEXT,
    destino_ruta_texto TEXT,
    distancia REAL,
    direccion_origen TEXT NOT NULL,
    latitud_origen REAL,
    longitud_origen REAL,
    direccion_destino TEXT,
    latitud_destino REAL,
    longitud_destino REAL
);

CREATE TABLE solicitudes (
    id_solicitud INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora_solicitud DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    fecha_hora_requerida DATETIME,
    cantidad_pasajero_carga REAL,
    id_cliente INTEGER NOT NULL,
    id_tipo_servicio INTEGER NOT NULL,
    id_estado_solicitud INTEGER NOT NULL,
    id_ruta INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_tipo_servicio) REFERENCES tipos_servicio(id_tipo_servicio),
    FOREIGN KEY (id_estado_solicitud) REFERENCES estados_solicitud(id_estado_solicitud),
    FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta)
);

CREATE TABLE asignaciones (
    id_asignacion INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora_inicio_asignacion DATETIME NOT NULL,
    fecha_hora_fin_asignacion DATETIME,
    precio_final REAL,
    id_solicitud INTEGER NOT NULL,
    id_conductor INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_conductor),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
);

CREATE TABLE cotizaciones_carga_mudanza (
    id_cotizacion INTEGER PRIMARY KEY AUTOINCREMENT,
    volumen_estimado REAL,
    peso_estimado REAL,
    distancia_estimada REAL,
    precio_estimado REAL,
    id_tipo_carga INTEGER,
    instrucciones_especiales TEXT,
    fecha_cotizacion DATE,
    id_solicitud INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    FOREIGN KEY (id_tipo_carga) REFERENCES tipos_carga(id_tipo_carga),
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE horarios_rutas (
    id_horario_ruta INTEGER PRIMARY KEY AUTOINCREMENT,
    hora_salida TIME,
    dias_semanas TEXT,
    id_ruta INTEGER NOT NULL,
    FOREIGN KEY (id_ruta) REFERENCES rutas(id_ruta)
);

CREATE TABLE incidente_emergencia (
    id_incidente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tipo_incidente INTEGER NOT NULL,
    direccion_ubicacion TEXT NOT NULL,
    latitud_ubicacion REAL,
    longitud_ubicacion REAL,
    descripcion_problema TEXT,
    fecha_hora_reporte DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    id_estado_incidente INTEGER,
    primeros_auxilios_requeridos BOOLEAN DEFAULT FALSE NOT NULL,
    id_solicitud INTEGER NOT NULL,
    FOREIGN KEY (id_tipo_incidente) REFERENCES tipos_incidente(id_tipo_incidente),
    FOREIGN KEY (id_estado_incidente) REFERENCES estados_incidente(id_estado_incidente),
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud)
);

CREATE TABLE asignaciones_emergencia (
    id_asignacion_emergencia INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_asignacion DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    fecha_resolucion DATETIME,
    id_incidente INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    id_conductor INTEGER NOT NULL,
    FOREIGN KEY (id_incidente) REFERENCES incidente_emergencia(id_incidente),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_conductor)
);

CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_viaje DATE NOT NULL,
    cantidad_asientos INTEGER NOT NULL,
    id_estado_reserva INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_solicitud INTEGER NOT NULL,
    id_horario_ruta INTEGER NOT NULL,
    FOREIGN KEY (id_estado_reserva) REFERENCES estados_reserva(id_estado_reserva),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_horario_ruta) REFERENCES horarios_rutas(id_horario_ruta)
);

CREATE TABLE transacciones_pago (
    -- UUID se manejará en Python y se almacenará como TEXT en SQLite
    id_transaccion TEXT PRIMARY KEY,
    monto REAL NOT NULL,
    id_moneda INTEGER NOT NULL,
    id_tipo_metodo_pago INTEGER NOT NULL,
    id_canal_pago INTEGER,
    id_estado_pago INTEGER NOT NULL,
    fecha_hora_transaccion DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    id_transaccion_proveedor TEXT UNIQUE,
    id_solicitud INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    FOREIGN KEY (id_moneda) REFERENCES monedas(id_moneda),
    FOREIGN KEY (id_tipo_metodo_pago) REFERENCES tipos_metodo_pago(id_tipo_metodo_pago),
    FOREIGN KEY (id_canal_pago) REFERENCES canales_pago(id_canal_pago),
    FOREIGN KEY (id_estado_pago) REFERENCES estados_pago(id_estado_pago),
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE auditoria (
    id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_creacion DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    fecha_ultima_modificacion DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    usuario_ultima_modificacion_id INTEGER NOT NULL,
    usuario_creacion_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_ultima_modificacion_id) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (usuario_creacion_id) REFERENCES usuarios(id_usuario)
);

CREATE TABLE conductor_servicio (
    id_conductor INTEGER NOT NULL,
    id_tipo_servicio INTEGER NOT NULL,
    fecha_habilitacion DATE,
    PRIMARY KEY (id_conductor, id_tipo_servicio),
    FOREIGN KEY (id_conductor) REFERENCES conductores(id_conductor),
    FOREIGN KEY (id_tipo_servicio) REFERENCES tipos_servicio(id_tipo_servicio)
);

CREATE TABLE IF NOT EXISTS registro_actividades (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    accion TEXT NOT NULL,
    recurso_afectado_tipo TEXT,
    recurso_afectado_id INTEGER,
    fecha_hora DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) NOT NULL,
    detalles_json TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

-- ******************************************************************************
-- INSERCIÓN DE DATOS INICIALES EN LAS TABLAS DE CATÁLOGO
-- ******************************************************************************

-- Tipos de Cliente
INSERT INTO tipos_cliente (nombre) VALUES
('Individual'),
('Empresa');

-- Estados de Conductor
INSERT INTO estados_conductor (nombre) VALUES
('Disponible'),
('Ocupado'),
('En Descanso'),
('Inactivo');

-- Tipos de Vehículo
INSERT INTO tipos_vehiculo (nombre, capacidad_maxima_pasajero, capacidad_maxima_carga, capacidad_maxima_volumen) VALUES
('Automóvil', 4, 100, 0.5),
('Camión de Carga', 2, 5000, 15.0),
('Ómnibus', 40, NULL, NULL),
('Moto', 1, 10, 0.1),
('Grúa', 2, NULL, NULL);

-- Estados de Vehículo
INSERT INTO estados_vehiculo (nombre) VALUES
('Operativo'),
('En Mantenimiento'),
('Fuera de Servicio'),
('Dañado');

-- Tipos de Servicio
INSERT INTO tipos_servicio (nombre, descripcion, es_colectivo) VALUES
('Transporte Individual', 'Transporte de pasajeros personalizable', 0),
('Carga de Contenedores', 'Transporte de grandes volúmenes de carga', 0),
('Mudanza', 'Servicio de traslado de bienes de hogar/oficina', 0),
('Emergencia en Vía', 'Asistencia en carretera, grúa, etc.', 0),
('Reserva de Ómnibus', 'Reserva de asientos en rutas predefinidas', 1);

-- Estados de Solicitud
INSERT INTO estados_solicitud (nombre) VALUES
('Pendiente'),
('Asignada'),
('En Curso'),
('Completada'),
('Cancelada');

-- Tipos de Carga
INSERT INTO tipos_carga (nombre, descripcion) VALUES
('General', 'Carga estándar sin requerimientos especiales'),
('Frágil', 'Requiere manejo cuidadoso'),
('Peligrosa', 'Materiales peligrosos con regulación especial'),
('Perecedera', 'Requiere control de temperatura'),
('Voluminosa', 'Carga grande pero no necesariamente pesada');

-- Tipos de Incidente
INSERT INTO tipos_incidente (nombre) VALUES
('Accidente'),
('Avería Mecánica'),
('Emergencia Médica'),
('Violencia'),
('Robo');

-- Estados de Incidente
INSERT INTO estados_incidente (nombre) VALUES
('Reportado'),
('En Atención'),
('Resuelto'),
('Cerrado');

-- Estados de Reserva
INSERT INTO estados_reserva (nombre) VALUES
('Pendiente'),
('Confirmada'),
('Cancelada'),
('Completada');

-- Monedas
INSERT INTO monedas (codigo, nombre) VALUES
('CUP', 'Peso Cubano'),
('MLC', 'Moneda Libremente Convertible'),
('USD', 'Dólar Estadounidense'),
('EUR', 'Euro');

-- Tipos de Método de Pago
INSERT INTO tipos_metodo_pago (nombre) VALUES
('Efectivo'),
('Transferencia Bancaria'),
('Tarjeta de Crédito'),
('Monedero Electrónico');

-- Canales de Pago
INSERT INTO canales_pago (nombre, descripcion) VALUES
('EnZona', 'Plataforma de pago cubana'),
('Transfermóvil', 'Aplicación bancaria cubana'),
('Pasarela Externa X', 'Proveedor de pago internacional'),
('TPV Físico', 'Terminal de punto de venta físico');

-- Estados de Pago
INSERT INTO estados_pago (nombre) VALUES
('Pendiente'),
('Completado'),
('Fallido'),
('Reembolsado'),
('En Proceso');

-- Tipos de Tarifa
INSERT INTO tipos_tarifa (nombre, descripcion) VALUES
('Por Km', 'Tarifa basada en la distancia recorrida'),
('Por Tiempo', 'Tarifa basada en la duración del servicio'),
('Tarifa Fija', 'Precio preestablecido para una ruta o servicio'),
('Tarifa por Paquete', 'Tarifa por el tipo de paquete/servicio de carga');
