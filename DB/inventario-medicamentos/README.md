# Sistema de Inventario de Medicamentos

Un **sistema profesional de caja registradora** para farmacias con:
- ✅ Gestión de inventario automatizada
- ✅ Punto de venta (POS)
- ✅ Escaneo de códigos de barras (GTIN)
- ✅ Consulta a APIs externas (Google + OpenFoodFacts)
- ✅ Múltiples interfaces: Terminal, GUI y Web
- ✅ Base de datos local SQLite (por defecto)
- ✅ Reportes en tiempo real

## 📋 Requisitos Previos

### Software Requerido
- **Python 3.8+**
- **SQLite** (incluido con Python)
- **Git** (opcional)

### Instalación de Python
Descarga desde: https://www.python.org/downloads/

## 🚀 Instalación Rápida

### 1. Descargar el Proyecto
```bash
cd Mi-Learning-of-code/DB
cd inventario-medicamentos
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

#### Opción recomendada: SQLite local (predeterminado)
1. Edita el archivo `.env` en la raíz:
```env
DB_ENGINE=sqlite
SQLITE_FILE=./inventario.db
```
2. Ejecuta la aplicación:
```bash
python main.py
```

#### Opción alternativa: MySQL con XAMPP
1. Edita `.env` y configura:
```env
DB_ENGINE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=     # Deja vacío si no tienes contraseña
MYSQL_DATABASE=inventario_medicamentos
```
2. Si usas MySQL, crea la base de datos en XAMPP / MySQL:
```bash
mysql -u root
CREATE DATABASE inventario_medicamentos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Ejecutar la Aplicación
```bash
python main.py
```

## 📱 Interfaces Disponibles

### 1. **Terminal (CLI)** - Interfaz de Línea de Comandos
```bash
# Opción 1 en el menú principal
```
- Menú interactivo en la terminal
- Rápido y eficiente
- Ideal para escaneo contínuo

### 2. **Interfaz Gráfica (GUI)** - PyQt5
```bash
# Opción 2 en el menú principal
```
- Interfaz visual profesional
- Muy intuitiva
- Requiere PyQt5 (incluido en requirements.txt)

### 3. **Interfaz Web** - Flask
```bash
# Opción 3 en el menú principal
# Luego abre: http://localhost:5000
```
- Accesible desde cualquier dispositivo
- Interfaz responsiva
- Ideal para múltiples usuarios

## 📦 Estructura del Proyecto

```
inventario-medicamentos/
├── config/              # Configuración
│   ├── __init__.py
│   └── settings.py      # Variables globales
├── database/            # Base de datos
│   ├── __init__.py
│   ├── connection.py    # Conexión a BD
│   └── models.py        # Modelos SQLAlchemy
├── api/                 # Integraciones externas
│   ├── __init__.py
│   ├── gtin_lookup.py   # Búsqueda de GTIN (OpenFoodFacts + Google)
│   └── google_api.py    # API de Google personalizada
├── core/                # Lógica principal
│   ├── __init__.py
│   ├── barcode_scanner.py     # Lectura de códigos
│   ├── inventory_manager.py   # Gestión de inventario
│   └── pos_manager.py         # Punto de venta
├── ui/                  # Interfaces de usuario
│   ├── __init__.py
│   ├── terminal_ui.py   # Terminal
│   └── gui_ui.py        # GUI (PyQt5)
├── web/                 # Interfaz web
│   ├── __init__.py
│   ├── app.py           # Aplicación Flask + API REST
│   ├── templates/       # Plantillas HTML
│   │   ├── index.html
│   │   ├── inventario.html
│   │   ├── pos.html
│   │   └── reportes.html
│   └── static/          # CSS, JS, imágenes
├── data/                # Archivos de datos
├── main.py              # Punto de entrada
├── requirements.txt     # Dependencias
├── .env                 # Configuración (NO commitar)
└── README.md           # Este archivo
```

## 🎯 Funcionalidades Principales

### A. 📦 Gestión de Inventario
- Registrar nuevos productos
- Buscar por GTIN (escaneo de código de barras)
- Consulta automática a APIs (Google + OpenFoodFacts)
- Agregar múltiples presentaciones (tableta, ampolla, cápsula, etc.)
- Registrar entrada/salida de stock
- Alertas de stock bajo
- Historial de movimientos

### B. 🛒 Punto de Venta (POS)
- Carrito de compra dinámico
- Escaneo rápido de productos
- Aplicación de descuentos
- Cálculo automático de impuestos (IVA 19%)
- Múltiples métodos de pago
- Generación de tickets
- Histórico de ventas

### C. 📊 Reportes
- Reporte general de inventario
- Reporte de ventas diarias
- Productos con stock bajo
- Valor total del inventario
- Análisis por método de pago

## 🔑 Características Técnicas

### Base de Datos
- **Motor**: SQLite local (por defecto), MySQL opcional
- **ORM**: SQLAlchemy
- **Modelos**:
  - Productos
  - Presentaciones
  - Movimientos de Inventario
  - Ventas
  - Usuarios

### APIs Integradas
- **OpenFoodFacts** (Gratuita): Búsqueda de medicamentos por GTIN
- **Google Custom Search** (Opcional): Búsqueda avanzada con imágenes

### Seguridad
- Validación de GTINs
- Verificación de dígito de control
- Manejo de errores robusto
- Logging completo

## 🛠️ Comandos Útiles

### Crear tablas en la BD
```bash
python -c "from database.connection import init_db; init_db()"
```

### Ver logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Backup de la base de datos
Para SQLite, simplemente copia el archivo `inventario.db`.

#### Backup de MySQL (opcional)
```bash
# Windows
"C:\xampp\mysql\bin\mysqldump" -u root inventario_medicamentos > backup.sql

# Linux
mysqldump -u root inventario_medicamentos > backup.sql
```

#### Restaurar backup de MySQL
```bash
mysql -u root inventario_medicamentos < backup.sql
```

## 📝 Guía Rápida de Uso

### Terminal
1. Inicia con `python main.py`
2. Selecciona opción `1` (Terminal)
3. Usa las opciones del menú
4. Escanea códigos de barras para operaciones rápidas

### GUI
1. Inicia con `python main.py`
2. Selecciona opción `2` (GUI)
3. Usa la interfaz visual intuitiva

### Web
1. Inicia con `python main.py`
2. Selecciona opción `3` (Web)
3. Abre `http://localhost:5000` en tu navegador
4. Accede desde cualquier dispositivo en la red

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### Error: "No se puede conectar a MySQL"
- Si usas MySQL, verifica que XAMPP esté corriendo
- Comprueba las credenciales en `.env`
- Verifica que la BD exista
- Si usas SQLite no necesitas servidor MySQL

### Error: "PyQt5 is not installed"
```bash
pip install PyQt5
```

### Error: "Flask is not installed"
```bash
pip install flask
```

## 📞 Soporte

Para reportar bugs o sugerir mejoras:
1. Crea un issue en GitHub
2. Describe el problema claramente
3. Incluye logs de error

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT.

## 🎓 Aprendizaje

Este proyecto cubre:
- Python avanzado (OOP, decoradores, context managers)
- Bases de datos (SQL, SQLAlchemy, normalizacion)
- APIs REST (Flask, JSON)
- GUI (PyQt5)
- Web scraping (BeautifulSoup)
- Integración con APIs externas
- Patrones de diseño (MVC, Factory)
- Testing y validación

## 🚀 Roadmap Futuro

- [ ] Autenticación de usuarios
- [ ] Exportación a PDF/Excel
- [ ] Sincronización en tiempo real (WebSockets)
- [ ] Aplicación móvil (React Native)
- [ ] Integración con código QR
- [ ] Sistema de proveedores
- [ ] Control de lotes y vencimiento
- [ ] Auditoría completa

---

**Última actualización**: 31 de mayo de 2025
**Versión**: 1.0.0
