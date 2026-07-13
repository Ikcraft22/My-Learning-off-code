"""
Interfaz Gráfica (GUI) con PyQt5 para el sistema de inventario.
Proporciona una interfaz visual profesional con:
- Gestión de inventario
- Punto de venta (POS)
- Reportes en tiempo real
"""

import logging
from typing import Optional
from datetime import datetime
import random

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
        QComboBox, QSpinBox, QDoubleSpinBox, QDialog, QDialogButtonBox,
        QMessageBox, QTabWidget, QListWidget, QListWidgetItem,
        QSplitter, QStatusBar, QFormLayout, QStackedWidget
    )
    from PyQt5.QtCore import Qt, QSize
    from PyQt5.QtGui import QIcon, QFont, QColor
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False
    print("⚠️ PyQt5 no está instalado. Use: pip install PyQt5")

from database.connection import SessionLocal, init_db
from core.barcode_scanner import EscanerProducto
from core.inventory_manager import GestorInventario
from core.pos_manager import GestorPOS
from config.settings import PRESENTACIONES, MONEDA

logger = logging.getLogger(__name__)

class InterfazGUI:
    """Interfaz Gráfica del Sistema de Inventario"""
    
    def __init__(self):
        """Inicializa la interfaz gráfica"""
        if not PYQT5_AVAILABLE:
            raise ImportError("PyQt5 es requerido para la interfaz gráfica")
        
        self.app = QApplication([])
        init_db()
        self.ventana_principal = VentanaPrincipal()
        self.db = SessionLocal()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        self.ventana_principal.show()
        self.app.exec_()


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        """Inicializa la ventana principal"""
        super().__init__()
        
        self.setWindowTitle("Sistema de Inventario de Medicamentos")
        self.setGeometry(100, 100, 1200, 800)
        
        # Inicializar gestores
        self.db = SessionLocal()
        self.inventario = GestorInventario(self.db)
        self.pos = GestorPOS(self.db)
        self.escaneo = EscanerProducto()
        
        # Crear interfaz
        self.crear_ui()
    
    def crear_ui(self):
        """Crea la interfaz de usuario"""
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Crear pestañas
        pestanas = QTabWidget()
        
        # Pestaña de Inventario
        pestanas.addTab(self.crear_pestaña_inventario(), "📦 Inventario")
        
        # Pestaña de POS
        pestanas.addTab(self.crear_pestaña_pos(), "🛒 POS")
        
        # Pestaña de Reportes
        pestanas.addTab(self.crear_pestaña_reportes(), "📊 Reportes")
        
        # Mostrar POS como primera pestaña activa
        pestanas.setCurrentIndex(1)
        
        layout = QVBoxLayout()
        layout.addWidget(pestanas)
        widget_central.setLayout(layout)
        
        # Barra de estado
        self.statusBar().showMessage("Listo")
    
    def crear_pestaña_inventario(self) -> QWidget:
        """Crea la pestaña de inventario"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Buscar producto
        layout_busqueda = QHBoxLayout()
        layout_busqueda.addWidget(QLabel("GTIN:"))
        self.entrada_gtin = QLineEdit()
        self.entrada_gtin.setPlaceholderText("Escanea o ingresa el GTIN")
        layout_busqueda.addWidget(self.entrada_gtin)
        
        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.clicked.connect(self.buscar_producto)
        layout_busqueda.addWidget(btn_buscar)
        
        btn_ver_todos = QPushButton("📋 Ver Todos")
        btn_ver_todos.clicked.connect(self.ver_todos_productos)
        layout_busqueda.addWidget(btn_ver_todos)
        
        layout.addLayout(layout_busqueda)
        
        # Tabla de productos
        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setColumnCount(6)
        self.tabla_inventario.setHorizontalHeaderLabels(
            ["GTIN", "Nombre", "Laboratorio", "Presentación", "Stock", "Precio"]
        )
        layout.addWidget(self.tabla_inventario)
        
        # Botones de acción
        layout_botones = QHBoxLayout()
        
        btn_nuevo = QPushButton("➕ Nuevo Producto")
        btn_nuevo.clicked.connect(self.abrir_dialogo_nuevo_producto)
        layout_botones.addWidget(btn_nuevo)
        
        btn_entrada = QPushButton("➡️  Entrada de Stock")
        btn_entrada.clicked.connect(self.registrar_entrada)
        layout_botones.addWidget(btn_entrada)
        
        btn_salida = QPushButton("⬅️  Salida de Stock")
        btn_salida.clicked.connect(self.registrar_salida)
        layout_botones.addWidget(btn_salida)
        
        layout.addLayout(layout_botones)
        
        self.ver_todos_productos()
        widget.setLayout(layout)
        return widget
    
    def crear_pestaña_pos(self) -> QWidget:
        """Crea la pestaña de punto de venta"""
        widget = QWidget()
        layout = QHBoxLayout()
        
        # Panel izquierdo: Búsqueda de productos
        layout_izquierda = QVBoxLayout()
        
        layout_izquierda.addWidget(QLabel("Agregar Producto al Carrito"))
        
        layout_busqueda = QHBoxLayout()
        self.entrada_gtin_pos = QLineEdit()
        self.entrada_gtin_pos.setPlaceholderText("Escanea o ingresa GTIN")
        layout_busqueda.addWidget(self.entrada_gtin_pos)
        
        btn_agregar = QPushButton("➕ Agregar")
        btn_agregar.clicked.connect(self.agregar_a_carrito_gui)
        layout_busqueda.addWidget(btn_agregar)
        
        # Enfocar el campo de GTIN para escaneo inmediato
        self.entrada_gtin_pos.setFocus()
        
        layout_izquierda.addLayout(layout_busqueda)
        
        # Panel derecho: Carrito
        layout_derecha = QVBoxLayout()
        
        layout_derecha.addWidget(QLabel("Carrito de Compra"))
        
        self.tabla_carrito = QTableWidget()
        self.tabla_carrito.setColumnCount(5)
        self.tabla_carrito.setHorizontalHeaderLabels(
            ["Producto", "Presentación", "Cantidad", "Precio", "Subtotal"]
        )
        layout_derecha.addWidget(self.tabla_carrito)
        
        # Resumen
        layout_resumen = QVBoxLayout()
        self.label_subtotal = QLabel(f"Subtotal: {MONEDA}0.00")
        self.label_impuesto = QLabel(f"Impuesto: {MONEDA}0.00")
        self.label_total = QLabel(f"Total: {MONEDA}0.00")
        
        layout_resumen.addWidget(self.label_subtotal)
        layout_resumen.addWidget(self.label_impuesto)
        layout_resumen.addWidget(self.label_total)
        
        layout_derecha.addLayout(layout_resumen)
        
        # Botones
        layout_botones_pos = QHBoxLayout()
        
        btn_eliminar = QPushButton("🗑️  Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_del_carrito_gui)
        layout_botones_pos.addWidget(btn_eliminar)
        
        btn_vaciar = QPushButton("🗑️  Vaciar Carrito")
        btn_vaciar.clicked.connect(self.vaciar_carrito_gui)
        layout_botones_pos.addWidget(btn_vaciar)
        
        btn_pagar = QPushButton("💳 Procesar Pago")
        btn_pagar.setStyleSheet("background-color: green; color: white;")
        btn_pagar.clicked.connect(self.procesar_pago_gui)
        layout_botones_pos.addWidget(btn_pagar)
        
        layout_derecha.addLayout(layout_botones_pos)
        
        layout.addLayout(layout_izquierda, 1)
        layout.addLayout(layout_derecha, 1)
        
        widget.setLayout(layout)
        return widget
    
    def crear_pestaña_reportes(self) -> QWidget:
        """Crea la pestaña de reportes"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("📊 Reportes del Sistema"))
        
        btn_reporte_inventario = QPushButton("Reporte de Inventario")
        btn_reporte_inventario.clicked.connect(self.generar_reporte_inventario)
        layout.addWidget(btn_reporte_inventario)
        
        btn_reporte_ventas = QPushButton("Reporte de Ventas")
        btn_reporte_ventas.clicked.connect(self.generar_reporte_ventas)
        layout.addWidget(btn_reporte_ventas)
        
        self.texto_reporte = QLabel()
        layout.addWidget(self.texto_reporte)
        
        widget.setLayout(layout)
        return widget
    
    def buscar_producto(self):
        """Busca un producto"""
        gtin = self.entrada_gtin.text().strip()
        if not gtin:
            QMessageBox.warning(self, "Advertencia", "Ingresa un GTIN")
            return
        
        producto = self.inventario.obtener_producto_por_gtin(gtin)
        
        if producto:
            self.tabla_inventario.setRowCount(0)
            for presentacion in producto.presentaciones:
                fila = self.tabla_inventario.rowCount()
                self.tabla_inventario.insertRow(fila)
                
                self.tabla_inventario.setItem(fila, 0, QTableWidgetItem(producto.gtin))
                self.tabla_inventario.setItem(fila, 1, QTableWidgetItem(producto.nombre))
                self.tabla_inventario.setItem(fila, 2, QTableWidgetItem(producto.laboratorio or ""))
                self.tabla_inventario.setItem(fila, 3, QTableWidgetItem(presentacion.tipo.value))
                self.tabla_inventario.setItem(fila, 4, QTableWidgetItem(str(presentacion.stock_actual)))
                self.tabla_inventario.setItem(fila, 5, QTableWidgetItem(f"{MONEDA}{presentacion.precio_venta}"))
        else:
            QMessageBox.information(self, "Información", f"Producto no encontrado: {gtin}")

    def ver_todos_productos(self):
        """Carga todos los productos en la tabla de inventario"""
        productos = self.inventario.obtener_productos()
        self.tabla_inventario.setRowCount(0)

        if not productos:
            QMessageBox.information(self, "Información", "No hay productos registrados.")
            return

        for producto in productos:
            for presentacion in producto.presentaciones:
                fila = self.tabla_inventario.rowCount()
                self.tabla_inventario.insertRow(fila)
                self.tabla_inventario.setItem(fila, 0, QTableWidgetItem(producto.gtin))
                self.tabla_inventario.setItem(fila, 1, QTableWidgetItem(producto.nombre))
                self.tabla_inventario.setItem(fila, 2, QTableWidgetItem(producto.laboratorio or ""))
                self.tabla_inventario.setItem(fila, 3, QTableWidgetItem(presentacion.tipo.value))
                self.tabla_inventario.setItem(fila, 4, QTableWidgetItem(str(presentacion.stock_actual)))
                self.tabla_inventario.setItem(fila, 5, QTableWidgetItem(f"{MONEDA}{presentacion.precio_venta}"))

    def abrir_dialogo_nuevo_producto(self):
        """Abre el diálogo para crear un nuevo producto"""
        dialogo = DialogoNuevoProducto(self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.obtener_datos()
            producto = self.inventario.registrar_producto(
                gtin=datos['gtin'],
                nombre=datos['nombre'],
                laboratorio=datos['laboratorio'],
                descripcion=datos['descripcion']
            )

            if not producto:
                QMessageBox.warning(self, "Error", "No se pudo crear el producto. Verifica los datos e inténtalo de nuevo.")
                return

            presentacion = self.inventario.agregar_presentacion(
                producto_id=producto.id,
                tipo_presentacion=datos['presentacion'],
                cantidad=datos['cantidad'],
                precio_unitario=datos['precio_unitario'],
                precio_venta=datos['precio_venta'],
                stock_inicial=datos['stock_inicial']
            )

            if not presentacion:
                QMessageBox.warning(self, "Error", "El producto se creó, pero no se pudo agregar la presentación.")
                return

            QMessageBox.information(self, "Éxito", "Producto creado correctamente.")
            self.entrada_gtin.setText(producto.gtin)
            self.buscar_producto()
    
    def registrar_entrada(self):
        """Registra una entrada de stock"""
        QMessageBox.information(self, "Información", "Funcionalidad de entrada aún en desarrollo")
    
    def registrar_salida(self):
        """Registra una salida de stock"""
        QMessageBox.information(self, "Información", "Funcionalidad de salida aún en desarrollo")
    
    def agregar_a_carrito_gui(self):
        """Agrega un producto al carrito desde GUI"""
        QMessageBox.information(self, "Información", "Funcionalidad de agregar a carrito aún en desarrollo")
    
    def eliminar_del_carrito_gui(self):
        """Elimina un producto del carrito"""
        QMessageBox.information(self, "Información", "Funcionalidad de eliminar aún en desarrollo")
    
    def vaciar_carrito_gui(self):
        """Vacía el carrito"""
        self.pos.carrito.vaciar_carrito()
        self.tabla_carrito.setRowCount(0)
        self.actualizar_resumen_carrito()
    
    def procesar_pago_gui(self):
        """Procesa el pago"""
        QMessageBox.information(self, "Información", "Funcionalidad de pago aún en desarrollo")
    
    def actualizar_resumen_carrito(self):
        """Actualiza el resumen del carrito"""
        resumen = self.pos.carrito.obtener_resumen()
        self.label_subtotal.setText(f"Subtotal: {MONEDA}{resumen['subtotal']:.2f}")
        self.label_impuesto.setText(f"Impuesto: {MONEDA}{resumen['impuesto']:.2f}")
        self.label_total.setText(f"Total: {MONEDA}{resumen['total']:.2f}")
    
    def generar_reporte_inventario(self):
        """Genera reporte de inventario"""
        reporte = self.inventario.reporte_general()
        texto = f"""
        Reporte de Inventario
        Fecha: {reporte['fecha']}
        
        Total de Productos: {reporte['total_productos']}
        Stock Total: {reporte['total_stock']} unidades
        Valor Inventario: {MONEDA}{reporte['valor_inventario']:.2f}
        Productos sin Stock: {reporte['productos_sin_stock']}
        Productos en Alerta: {reporte['productos_alerta']}
        """
        self.texto_reporte.setText(texto)
    
    def generar_reporte_ventas(self):
        """Genera reporte de ventas"""
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        reporte = self.pos.reporte_ventas_diario(fecha_hoy)
        
        texto = f"""
        Reporte de Ventas del {fecha_hoy}
        
        Cantidad de Ventas: {reporte['cantidad_ventas']}
        Total de Ventas: {MONEDA}{reporte['total_ventas']:.2f}
        Promedio por Venta: {MONEDA}{reporte['promedio_venta']:.2f}
        Impuestos Total: {MONEDA}{reporte['impuestos_totales']:.2f}
        
        Métodos de Pago:
        {chr(10).join([f"  {k}: {MONEDA}{v:.2f}" for k, v in reporte['metodos_pago'].items()])}
        """
        self.texto_reporte.setText(texto)


class DialogoNuevoProducto(QDialog):
    """Diálogo para crear un nuevo producto y su presentación"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Producto")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.campo_gtin = QLineEdit()
        self.campo_nombre = QLineEdit()
        self.campo_laboratorio = QLineEdit()
        self.campo_descripcion = QLineEdit()
        self.campo_presentacion = QComboBox()
        self.campo_presentacion.addItems([v['nombre'] for v in PRESENTACIONES.values()])
        self.campo_presentacion.currentTextChanged.connect(self.actualizar_label_precio)
        self.campo_presentacion.currentTextChanged.connect(self.actualizar_subseccion)
        self.presentaciones_por_nombre = {v['nombre']: k for k, v in PRESENTACIONES.items()}
        self.campo_cantidad = QSpinBox()
        self.campo_cantidad.setRange(1, 1000)
        self.campo_cantidad.setValue(1)
        self.campo_precio_unitario = QDoubleSpinBox()
        self.campo_precio_unitario.setRange(0.0, 1000000.0)
        self.campo_precio_unitario.setDecimals(2)
        self.campo_precio_unitario.setValue(0.0)
        self.campo_precio_venta = QDoubleSpinBox()
        self.campo_precio_venta.setRange(0.0, 1000000.0)
        self.campo_precio_venta.setDecimals(2)
        self.campo_precio_venta.setValue(0.0)
        self.label_precio_venta = QLabel("Precio caja:")
        self.campo_stock_inicial = QSpinBox()
        self.campo_stock_inicial.setRange(0, 10000)
        self.campo_stock_inicial.setValue(0)

        form.addRow("GTIN:", self.campo_gtin)
        form.addRow("Nombre:", self.campo_nombre)
        form.addRow("Laboratorio:", self.campo_laboratorio)
        form.addRow("Descripción:", self.campo_descripcion)
        form.addRow("Presentación:", self.campo_presentacion)
        form.addRow("Cantidad por envase:", self.campo_cantidad)
        form.addRow("Precio unidad:", self.campo_precio_unitario)
        form.addRow(self.label_precio_venta, self.campo_precio_venta)
        form.addRow("Stock inicial:", self.campo_stock_inicial)

        layout.addLayout(form)

        self.subseccion_presentacion = QStackedWidget()
        self.subseccion_presentacion.setMinimumHeight(110)
        for presentacion_nombre in PRESENTACIONES.values():
            widget_subseccion = QWidget()
            layout_subseccion = QVBoxLayout()
            label_subseccion = QLabel(f"Subsección para {presentacion_nombre['nombre']}.")
            label_subseccion.setWordWrap(True)
            layout_subseccion.addWidget(label_subseccion)
            layout_subseccion.addStretch()
            widget_subseccion.setLayout(layout_subseccion)
            self.subseccion_presentacion.addWidget(widget_subseccion)
        layout.addWidget(self.subseccion_presentacion)
        self.actualizar_subseccion(self.campo_presentacion.currentText())

        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.validar_y_aceptar)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        self.setLayout(layout)
        self.llenar_datos_aleatorios()

    def validar_y_aceptar(self):
        if not self.campo_gtin.text().strip():
            QMessageBox.warning(self, "Validación", "El GTIN es obligatorio.")
            return
        if not self.campo_nombre.text().strip():
            QMessageBox.warning(self, "Validación", "El nombre del producto es obligatorio.")
            return
        if self.campo_precio_venta.value() <= 0:
            QMessageBox.warning(self, "Validación", "El precio de presentación debe ser mayor que 0.")
            return
        self.accept()

    def actualizar_label_precio(self, texto_presentacion: str):
        nombre_presentacion = texto_presentacion.strip().lower()
        if nombre_presentacion:
            self.label_precio_venta.setText(f"Precio {nombre_presentacion}:")
        else:
            self.label_precio_venta.setText("Precio presentación:")

    def actualizar_subseccion(self, texto_presentacion: str):
        presentacion_nombre = texto_presentacion.strip()
        clave = self.presentaciones_por_nombre.get(presentacion_nombre)
        if clave is not None:
            index = list(PRESENTACIONES.keys()).index(clave)
            self.subseccion_presentacion.setCurrentIndex(index)
        else:
            self.subseccion_presentacion.setCurrentIndex(0)

    def llenar_datos_aleatorios(self):
        nombres_genericos = [
            "Amoxilina", "Clorfenamina", "Diclofenaco", "Loratadina", "Omeprazol",
            "Vitamina C", "Paracetamol", "Ibuprofeno", "Metformina", "Simvastatina"
        ]
        laboratorios = ["Laboratorios Genéricos", "Farmacia Central", "BioSalud", "Medix", "Laboratorios Vida"]
        descripciones = [
            "Medicamento genérico para uso diario",
            "Tratamiento estándar para síntomas leves",
            "Presentación económica en envase seguro",
            "Producto diseñado para alivio rápido",
            "Fórmula genérica para cuidado general"
        ]

        gtin_base = random.randint(7501000000000, 7501009999999)
        self.campo_gtin.setText(str(gtin_base))
        self.campo_nombre.setText(random.choice(nombres_genericos))
        self.campo_laboratorio.setText(random.choice(laboratorios))
        self.campo_descripcion.setText(random.choice(descripciones))
        self.campo_presentacion.setCurrentIndex(random.randint(0, self.campo_presentacion.count() - 1))
        self.campo_cantidad.setValue(random.randint(1, 3))
        self.campo_precio_unitario.setValue(round(random.uniform(10.0, 80.0), 2))
        self.campo_precio_venta.setValue(round(random.uniform(25.0, 150.0), 2))
        self.campo_stock_inicial.setValue(random.randint(10, 100))

    def obtener_datos(self):
        return {
            'gtin': self.campo_gtin.text().strip(),
            'nombre': self.campo_nombre.text().strip(),
            'laboratorio': self.campo_laboratorio.text().strip(),
            'descripcion': self.campo_descripcion.text().strip(),
            'presentacion': self.campo_presentacion.currentText().lower(),
            'cantidad': self.campo_cantidad.value(),
            'precio_unitario': self.campo_precio_unitario.value(),
            'precio_venta': self.campo_precio_venta.value(),
            'stock_inicial': self.campo_stock_inicial.value(),
        }


def ejecutar_interfaz_gui():
    """Punto de entrada para la interfaz gráfica"""
    try:
        interfaz = InterfazGUI()
        interfaz.ejecutar()
    except ImportError as e:
        print(f"❌ Error: {e}")
