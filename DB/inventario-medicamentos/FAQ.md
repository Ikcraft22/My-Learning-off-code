# GUÍA DE CONFIGURACIÓN - PREGUNTAS FRECUENTES

## ❓ ¿Cómo crear backups periódicos con XAMPP?

### Opción 1: Script Python Automatizado
```python
# backup_automatico.py
import os
import subprocess
from datetime import datetime

RUTA_MYSQLDUMP = r"C:\xampp\mysql\bin\mysqldump"
USUARIO = "root"
BD = "inventario_medicamentos"
CARPETA_BACKUPS = "./backups"

def crear_backup():
    if not os.path.exists(CARPETA_BACKUPS):
        os.makedirs(CARPETA_BACKUPS)
    
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_backup = f"{CARPETA_BACKUPS}/backup_{fecha}.sql"
    
    comando = f'{RUTA_MYSQLDUMP} -u {USUARIO} {BD} > {archivo_backup}'
    
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"✅ Backup creado: {archivo_backup}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear backup: {e}")

if __name__ == "__main__":
    crear_backup()
```

### Opción 2: Automatizar con Task Scheduler (Windows)
1. Abre **Task Scheduler**
2. Crea una nueva tarea
3. Establece el trigger (cada día, cada hora, etc.)
4. Acción: Ejecutar script Python

### Opción 3: Usar MySQL Workbench
1. Abre MySQL Workbench
2. Conecta a tu servidor
3. Server → Data Export
4. Selecciona la BD
5. Elige guardar en archivo SQL

## 🗄️ ¿Qué BD portátil usar?

### SQLite (Recomendado para Portabilidad)
```python
# Cambiar en config/settings.py
DATABASE_URL = "sqlite:///./inventario.db"  # Archivo único, muy portable
```
✅ Ventajas:
- Un archivo único
- No necesita servidor
- Perfecto para portátil/USB
- Backups super fáciles (solo copia el archivo)

❌ Desventajas:
- No es ideal para múltiples usuarios simultáneos
- Menos escalable

### MySQL (Recomendado para Producción)
✅ Ventajas:
- Multi-usuario
- Escalable
- Mejor rendimiento
- Backups profesionales

❌ Desventajas:
- Requiere servidor
- Más configuración

## 🔄 ¿Cómo migrarpara de CSV a BD?

```python
# scripts/importar_medicamentos.py
import pandas as pd
from database.connection import SessionLocal
from database.models import Producto, Presentacion
from core.inventory_manager import GestorInventario

def importar_csv(ruta_csv):
    """Importa medicamentos desde CSV a BD"""
    db = SessionLocal()
    inventario = GestorInventario(db)
    
    df = pd.read_csv(ruta_csv)
    
    for _, fila in df.iterrows():
        # Crear producto
        producto = inventario.registrar_producto(
            gtin=str(fila['GTIN_ASIGNADO']),
            nombre=fila['producto'],
            laboratorio=fila['titular'],
            descripcion=fila['principioactivo']
        )
        
        # Agregar presentación por defecto
        if producto:
            inventario.agregar_presentacion(
                producto_id=producto.id,
                tipo_presentacion="tableta",
                cantidad=1,
                precio_unitario=5000,  # Ajusta según tu país
                precio_venta=8000,
                stock_inicial=10
            )
    
    db.close()
    print("✅ Importación completada")

if __name__ == "__main__":
    importar_csv("CÓDIGO_ÚNICO_DE_MEDICAMENTOS_VIGENTES_20250922.csv")
```

## 🔐 Seguridad: Cambiar Contraseña MySQL

```sql
-- En MySQL
ALTER USER 'root'@'localhost' IDENTIFIED BY 'tu_nueva_contraseña';
FLUSH PRIVILEGES;
```

Luego actualiza `.env`:
```env
MYSQL_PASSWORD=tu_nueva_contraseña
```

## 📱 Usar en Múltiples Dispositivos

### Opción 1: Servidor Web (Recomendado)
```bash
# En la máquina servidor (tu computadora)
python main.py
# Selecciona opción 3 (Web)

# En otros dispositivos
http://tu_ip:5000
# Ejemplo: http://192.168.1.100:5000
```

Para encontrar tu IP:
```bash
# Windows (PowerShell)
ipconfig

# Linux/Mac
ifconfig
```

### Opción 2: Base de Datos Centralizada
Todos los clientes usan la misma BD MySQL en XAMPP.

## 🐳 Usar Docker (Avanzado)

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

```bash
# Construir imagen
docker build -t inventario-medicamentos .

# Ejecutar contenedor
docker run -p 5000:5000 inventario-medicamentos
```

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] XAMPP descargado e instalado
- [ ] MySQL iniciado en XAMPP
- [ ] Base de datos "inventario_medicamentos" creada
- [ ] requirements.txt instalado
- [ ] .env configurado correctamente
- [ ] Tablas creadas en la BD
- [ ] main.py ejecutándose sin errores

## 🆘 Debug: Activar Logging Completo

```python
# Al inicio de main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

## 📊 Ver BD en Tiempo Real

### MySQL Workbench (Recomendado)
1. Descarga desde mysql.com
2. Conecta a localhost:3306
3. Visualiza y edita datos

### phpMyAdmin (Incluido con XAMPP)
1. Abre XAMPP
2. Haz clic en "Admin" en MySQL
3. Abre http://localhost/phpmyadmin

## 🚀 Optimizaciones Recomendadas

```sql
-- Crear índices para búsqueda rápida
CREATE INDEX idx_gtin ON productos(gtin);
CREATE INDEX idx_nombre ON productos(nombre);
CREATE INDEX idx_stock ON presentaciones(stock_actual);

-- Ver tabla
SHOW INDEXES FROM productos;
```

---

**Última actualización**: 31 de mayo de 2025
