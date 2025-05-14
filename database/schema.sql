-- Tabla de empleados
CREATE TABLE empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    direccion TEXT NOT NULL,
    telefono TEXT NOT NULL,
    departamento TEXT NOT NULL,
    puesto TEXT NOT NULL
);

-- Tabla de activos
CREATE TABLE activos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_activo TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_compra TEXT NOT NULL,
    numero_factura TEXT NOT NULL,
    monto REAL NOT NULL,
    id_empleado INTEGER NOT NULL,
    FOREIGN KEY(id_empleado) REFERENCES empleados(id)
);

-- Tabla de usuarios con campo rol y vinculación a empleado
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'empleado',
    id_empleado INTEGER,
    FOREIGN KEY(id_empleado) REFERENCES empleados(id)
);

-- Usuarios de prueba
INSERT INTO usuarios (username, password, nombre, rol)
VALUES ('admin', '1234', 'Administrador General', 'admin');

