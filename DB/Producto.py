import pandas as pd
import time
import os

# --- CONFIGURACIÓN DE ARCHIVOS Y COLUMNAS ---
NOMBRE_ARCHIVO = "CÓDIGO_ÚNICO_DE_MEDICAMENTOS_VIGENTES_20250922.csv"

def buscar_producto_por_gtin(gtin: str):
    """
    Carga el CSV y busca el GTIN en las columnas 'GTIN_ASIGNADO' e 'IUM',
    forzando la lectura de identificadores como texto.
    """
    try:
        # Configuración de tipos para asegurar que los códigos se lean como texto
        dtype_config = {'IUM': str, 'GTIN_ASIGNADO': str}
        
        # Leemos el archivo
        df = pd.read_csv(NOMBRE_ARCHIVO, encoding='utf-8', low_memory=False, dtype=dtype_config)
        
        producto_encontrado = None
        
        # 1. Búsqueda en la columna GTIN_ASIGNADO
        if 'GTIN_ASIGNADO' in df.columns:
            filtro_gtin = df['GTIN_ASIGNADO'].astype(str) == gtin
            if filtro_gtin.any():
                producto_encontrado = df[filtro_gtin].iloc[0]

        # 2. Búsqueda en la columna IUM (si no se encontró en GTIN_ASIGNADO)
        if producto_encontrado is None and 'IUM' in df.columns:
            filtro_ium = df['IUM'].astype(str) == gtin
            if filtro_ium.any():
                producto_encontrado = df[filtro_ium].iloc[0]
                
        return producto_encontrado
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{NOMBRE_ARCHIVO}'. Asegúrate de que esté en la misma carpeta.")
        return None
    except Exception as e:
        print(f"❌ Error al cargar/procesar el archivo CSV: {e}")
        return None

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    print("--------------------------------------------------------------------------------")
    print("BUSCADOR DE PRODUCTOS POR GTIN")
    print("--------------------------------------------------------------------------------")
    
    while True:
        gtin = input("➡️ Ingresa el GTIN (código de barras) a buscar (o 'salir'): ").strip()
        
        if gtin.lower() == 'salir':
            print("¡Buscador finalizado!")
            break

        print(f"🔍 Buscando el GTIN: {gtin}...")
        
        producto = buscar_producto_por_gtin(gtin)
        
        if producto is not None:
            print("\n✅ ¡PRODUCTO ENCONTRADO!")
            print("----------------------------------------")
            
            # Imprimir información clave del producto
            print(f"Nombre del Producto: {producto['producto']}")
            print(f"Titular (Laboratorio): {producto['titular']}")
            print(f"Registro Sanitario: {producto['registrosanitario']}")
            print(f"Forma Farmacéutica: {producto['formafarmaceutica']}")
            print(f"Principio Activo: {producto['principioactivo']}")
            # ⚠️ La línea de Concentración separada ha sido eliminada para evitar el 'B g'.
            print(f"Estado del Registro: {producto['estadoregistro']}")
            
            print("----------------------------------------")
        else:
            print(f"\n⚠️ GTIN {gtin} no encontrado en el archivo.")
            
        time.sleep(1)