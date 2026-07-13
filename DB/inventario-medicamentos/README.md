# Sistema de Inventario de Medicamentos

Documentación actualizada el 13 de julio de 2026.

## Estado actual del proyecto

Este proyecto ya funciona como un sistema básico pero completo para la gestión de inventario y ventas de medicamentos, con soporte para:

- gestión de productos y presentaciones
- registro de movimientos de entrada/salida/ajuste
- punto de venta con tickets y métodos de pago
- búsqueda de información por GTIN
- interfaces por terminal, GUI y web
- base de datos SQLite por defecto, con soporte opcional para MySQL

## Requisitos

- Python 3.10 o superior
- pip
- SQLite (incluido con Python)
- opcional: PyQt5 para la interfaz gráfica

## Instalación rápida

1. Crear y activar un entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación
```bash
python main.py
```

## Uso de la aplicación

Al ejecutar el programa aparece un menú principal con estas opciones:

- 1. Terminal: interfaz de consola
- 2. GUI: interfaz gráfica con PyQt5
- 3. Web: servidor Flask en http://localhost:5000
- 4. Configuración: guía para usar SQLite o MySQL
- 5. Salir

## Configuración recomendada

Por defecto el proyecto usa SQLite y guarda la base en:

```env
DB_ENGINE=sqlite
SQLITE_FILE=./inventario.db
```

Si prefieres MySQL, puedes configurarlo en el archivo .env con:

```env
DB_ENGINE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=inventario_medicamentos
```

## Estructura principal

- config/: configuración general del proyecto
- database/: modelos SQLAlchemy y conexión a la base de datos
- core/: lógica de inventario, POS y escaneo
- api/: integraciones con GTIN y APIs externas
- ui/: interfaces terminal y GUI
- web/: aplicación Flask y endpoints REST
- data/: archivos de datos adicionales

## Funcionalidades ya incluidas

- registrar productos con GTIN, CUM y datos del laboratorio
- crear presentaciones con stock y precios
- registrar movimientos de inventario
- generar ventas y tickets
- consultar productos por GTIN
- mostrar reportes básicos de inventario y ventas
- exponer una API web para productos, inventario y ventas

## Notas importantes

- La base de datos se inicializa automáticamente al arrancar la app.
- La interfaz web se levanta con Flask y puede abrirse en el navegador.
- Si la GUI no funciona, revisa que PyQt5 esté instalado.

## Documentación adicional

- CHANGELOG.md: historial de cambios
- DOCUMENTACION_COMPLETA.md: guía técnica más amplia
- FAQ.md: preguntas frecuentes y soluciones


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
