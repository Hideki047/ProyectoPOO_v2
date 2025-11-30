CREATE DATABASE IF NOT EXISTS rentacar_seguro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE rentacar_seguro;

-- Tabla empleados
CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    cargo VARCHAR(20) NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    run VARCHAR(12) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

-- Tabla vehículos
CREATE TABLE IF NOT EXISTS vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patente VARCHAR(10) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio INT NOT NULL,
    precio_diario_uf DECIMAL(10,2) NOT NULL,
    estado ENUM('DISPONIBLE', 'ARRENDADO') NOT NULL DEFAULT 'DISPONIBLE'
);

-- Tabla arriendos
CREATE TABLE IF NOT EXISTS arriendos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehiculo_id INT NOT NULL,
    cliente_id INT NOT NULL,
    empleado_id INT NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    valor_uf DECIMAL(10,2) NOT NULL,
    total_uf DECIMAL(10,2) NOT NULL,
    total_clp DECIMAL(15,2) NOT NULL,
    estado ENUM('VIGENTE', 'CANCELADO', 'FINALIZADO') NOT NULL DEFAULT 'VIGENTE',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehiculo_id) REFERENCES vehiculos(id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id)
);
