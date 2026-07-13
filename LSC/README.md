# Reconocer y abrir cámaras (Python)

Pequeño script para enumerar dispositivos de cámara, seleccionar uno y abrirlo en una vista previa.

Requisitos:

- Python 3.8+
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
python main.py
```

El primer uso descargará automáticamente el modelo de MediaPipe en `models/holistic_landmarker.task`.

Controles dentro de la ventana de la cámara:

+- `q`: salir
+- `s`: guardar snapshot (imagen PNG)
+- `d`: alternar overlay de detección
+- `r`: iniciar/detener grabación de landmarks
