-- 1. Crear la base de datos
CREATE DATABASE IF NOT EXISTS hospital_system;
USE hospital_system;

-- 2. Crear la tabla de pacientes (necesaria para el Dashboard)
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20),
    allergy VARCHAR(255),
    phone VARCHAR(20)
);

-- 3. Tabla de Doctores
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    phone VARCHAR(20)
);

-- 4. Tabla de Citas Médicas
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATETIME,
    reason VARCHAR(255),
    status ENUM('Pendiente', 'Completada', 'Cancelada') DEFAULT 'Pendiente',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- 5. Historial Médico
CREATE TABLE IF NOT EXISTS medical_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    diagnosis TEXT,
    treatment TEXT,
    visit_date DATE,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- 6. Datos de prueba iniciales
INSERT IGNORE INTO patients (id, name, age, gender, allergy, phone) VALUES 
(1, 'Mariana Pérez', 28, 'Femenino', 'Penicilina', '555-0101'),
(2, 'Juan Torres', 45, 'Masculino', 'Ninguna', '555-0102');

INSERT IGNORE INTO doctors (id, name, specialty, phone) VALUES 
(1, 'Dr. Smith', 'Cardiología', '555-9988'),
(2, 'Dra. Casas', 'Pediatría', '555-7766');

INSERT IGNORE INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES 
(1, 1, '2023-12-01 10:00:00', 'Chequeo general'),
(2, 2, '2023-12-02 15:30:00', 'Control pediátrico');