-- =====================================================
-- FOODEXPRESS - BASE DE DATOS COMPLETA
-- Versión 2.0 con todos los módulos
-- =====================================================

DROP DATABASE IF EXISTS foodexpress_db;
CREATE DATABASE foodexpress_db;
USE foodexpress_db;

-- =====================================================
-- TABLA: usuarios (clientes, restaurantes, repartidores)
-- =====================================================
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    tipo ENUM('cliente', 'restaurante', 'repartidor') DEFAULT 'cliente',
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    codigo_2fa VARCHAR(10),
    codigo_2fa_expiracion DATETIME
);

-- =====================================================
-- TABLA: repartidores (datos específicos)
-- =====================================================
CREATE TABLE repartidores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    vehiculo ENUM('bicicleta', 'moto', 'carro') DEFAULT 'moto',
    licencia VARCHAR(50),
    ubicacion_lat DECIMAL(10,8),
    ubicacion_lng DECIMAL(11,8),
    disponible BOOLEAN DEFAULT TRUE,
    calificacion_promedio DECIMAL(2,1) DEFAULT 5.0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: productos (comidas de restaurantes)
-- =====================================================
CREATE TABLE productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurante_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    imagen VARCHAR(255),
    categoria VARCHAR(50),
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (restaurante_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: promociones (descuentos especiales)
-- =====================================================
CREATE TABLE promociones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    producto_id INT NOT NULL,
    descuento DECIMAL(5,2) NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: pedidos
-- =====================================================
CREATE TABLE pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    repartidor_id INT NULL,
    fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    estado ENUM('pendiente', 'pagado', 'preparando', 'asignado', 'en_camino', 'entregado', 'cancelado') DEFAULT 'pendiente',
    direccion_entrega TEXT NOT NULL,
    metodo_pago ENUM('tarjeta', 'nequi', 'efectivo') DEFAULT 'efectivo',
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (repartidor_id) REFERENCES repartidores(id)
);

-- =====================================================
-- TABLA: detalle_pedidos
-- =====================================================
CREATE TABLE detalle_pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- =====================================================
-- TABLA: carrito
-- =====================================================
CREATE TABLE carrito (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL DEFAULT 1,
    fecha_agregado DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- =====================================================
-- TABLA: pagos (registro de transacciones)
-- =====================================================
CREATE TABLE pagos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    metodo ENUM('tarjeta', 'nequi', 'efectivo') NOT NULL,
    referencia VARCHAR(100),
    estado ENUM('pendiente', 'completado', 'fallido', 'reembolsado') DEFAULT 'pendiente',
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

-- =====================================================
-- TABLA: tracking_repartidores (historial de ubicaciones)
-- =====================================================
CREATE TABLE tracking_repartidores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    repartidor_id INT NOT NULL,
    latitud DECIMAL(10,8) NOT NULL,
    longitud DECIMAL(11,8) NOT NULL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repartidor_id) REFERENCES repartidores(id)
);

-- =====================================================
-- DATOS DE EJEMPLO
-- =====================================================

-- Insertar restaurantes
INSERT INTO usuarios (nombre, email, password, telefono, direccion, tipo) VALUES
('La Burguer Queen', 'burguer@foodexpress.com', 'hashed_pass', '3001234567', 'Calle 1 #2-3', 'restaurante'),
('Pizza Hot', 'pizza@foodexpress.com', 'hashed_pass', '3001234568', 'Carrera 4 #5-6', 'restaurante'),
('Sushi Master', 'sushi@foodexpress.com', 'hashed_pass', '3001234569', 'Avenida 7 #8-9', 'restaurante');

-- Insertar clientes
INSERT INTO usuarios (nombre, email, password, telefono, direccion, tipo) VALUES
('Carlos Pérez', 'carlos@mail.com', 'hashed_pass', '3101234567', 'Calle 10 #20-30', 'cliente'),
('Ana Gómez', 'ana@mail.com', 'hashed_pass', '3101234568', 'Carrera 15 #25-35', 'cliente');

-- Insertar repartidores
INSERT INTO usuarios (nombre, email, password, telefono, direccion, tipo) VALUES
('Pedro Rodríguez', 'pedro@repartidor.com', 'hashed_pass', '3201234567', 'Calle 5 #10-15', 'repartidor'),
('Luis Martínez', 'luis@repartidor.com', 'hashed_pass', '3201234568', 'Carrera 8 #12-18', 'repartidor');

INSERT INTO repartidores (usuario_id, vehiculo, licencia, ubicacion_lat, ubicacion_lng, disponible) VALUES
(6, 'moto', 'LIC-001', 4.6097, -74.0817, TRUE),
(7, 'bicicleta', 'LIC-002', 4.6100, -74.0820, TRUE);

-- Insertar productos
INSERT INTO productos (restaurante_id, nombre, descripcion, precio, categoria) VALUES
(1, 'Hamburguesa Sencilla', 'Pan, carne, lechuga, tomate', 12500, 'Hamburguesas'),
(1, 'Hamburguesa Doble', 'Doble carne, queso, lechuga, tomate', 18900, 'Hamburguesas'),
(1, 'Papas Fritas', 'Papas crujientes', 5500, 'Acompañamientos'),
(2, 'Pizza Margarita', 'Salsa tomate, queso, albahaca', 25000, 'Pizzas'),
(2, 'Pizza Pepperoni', 'Salsa tomate, queso, pepperoni', 32000, 'Pizzas'),
(3, 'Roll de Salmón', 'Salmón fresco, arroz, algas', 18000, 'Sushi');

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================