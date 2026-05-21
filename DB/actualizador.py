import pandas as pd
import time
import os

# --- CONFIGURACIÓN DE ARCHIVOS Y COLUMNAS ---
NOMBRE_ARCHIVO = "CÓDIGO_ÚNICO_DE_MEDICAMENTOS_VIGENTES_20250922.csv"

# Columnas que añadiremos/gestionaremos en el CSV
NUEVAS_COLUMNAS = ['GTIN_ASIGNADO', 'NOMBRE_EXTRAIDO_GOOGLE', 'SNIPPET_GOOGLE'] 

# --- FUNCIÓN DE CARGA CORREGIDA PARA PREVENIR NOTACIÓN CIENTÍFICA ---
def cargar_csv():
    """
    Carga el CSV y fuerza la lectura de identificadores largos como texto (string)
    para prevenir la notación científica (e+).
    """
    try:
        # ⚠️ SOLUCIÓN CLAVE: Definimos los tipos de datos (dtype) para forzar TEXTO en identificadores largos.
        # Esto previene que Pandas interprete el GTIN como un número flotante (e+).
        dtype_config = {
            'IUM': str,
            'GTIN_ASIGNADO': str, 
            'expedientecum': str,
            'consecutivocum': str,
            'NOMBRE_EXTRAIDO_GOOGLE': str,
            'SNIPPET_GOOGLE': str          
        }
        
        # Leemos el CSV aplicando la configuración de tipos.
        df = pd.read_csv(NOMBRE_ARCHIVO, encoding='utf-8', low_memory=False, dtype=dtype_config)
        
        # Creamos la clave de búsqueda combinada (CUM Completo)
        df['CUM_COMPLETO'] = df['expedientecum'] + '-' + df['consecutivocum']
        
        # Asegura que las columnas de actualización existan y estén inicializadas como objeto/string
        for col in NUEVAS_COLUMNAS:
            if col not in df.columns:
                 df[col] = pd.Series(dtype='object')
        
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{NOMBRE_ARCHIVO}'. Asegúrate de que esté en la misma carpeta.")
        return None
    except Exception as e:
        print(f"❌ Error al cargar/procesar el archivo CSV: {e}")
        return None

# --- FUNCIÓN CON SOPORTE PARA BORRADO Y ASIGNACIÓN ---
def buscar_y_actualizar_producto(df):
    """
    Gestiona el flujo interactivo: pide GTIN, busca por palabra clave,
    y pide confirmación por CUM_COMPLETO. Permite usar 'BORRAR' como GTIN.
    """
    print("\n--- BÚSQUEDA Y ACTUALIZACIÓN INTERACTIVA ---")
    
    # 1. Entrada: GTIN (o palabra clave BORRAR)
    gtin = input("➡️ Ingresa el GTIN (o 'BORRAR' para limpiar una celda) a buscar (o 'salir'): ").strip()
    
    if gtin.lower() == 'salir':
        return False
        
    # 2. Entrada: Palabra Clave (para filtrar el CSV)
    keyword = input("➡️ Ingresa una PALABRA CLAVE ÚNICA del producto (ej: 'FLUTICASONA' o 'NOVAMED'): ").strip().upper()
    
    if not keyword:
        print("🛑 Palabra clave no ingresada. Cancelando.")
        return True

    print(f"🔎 Buscando por la palabra clave: '{keyword}'...")

    # 3. Filtrado del DataFrame
    # Se usa .str.upper() para asegurar que la búsqueda sea insensible a mayúsculas/minúsculas.
    filtro = (df['producto'].astype(str).str.upper().str.contains(keyword, na=False)) | \
             (df['titular'].astype(str).str.upper().str.contains(keyword, na=False))
             
    resultados = df[filtro].copy()

    if resultados.empty:
        print(f"⚠️ No se encontraron resultados que contengan '{keyword}'. Intenta con otra palabra.")
        return True

    # 4. Mostrar Resultados al Usuario
    print(f"\n✅ Se encontraron {len(resultados)} coincidencias. Identifica tu producto:")
    print("------------------------------------------------------------------------------------------------------------------------------------")
    # Mostrar solo las columnas relevantes
    print(resultados[['CUM_COMPLETO', 'producto', 'titular', 'GTIN_ASIGNADO']].to_string(index=False))
    print("------------------------------------------------------------------------------------------------------------------------------------")
    
    # 5. Confirmación por CUM_COMPLETO
    cum_a_actualizar = input("\n➡️ Ingresa el CUM COMPLETO exacto de la fila que deseas actualizar: ").strip()
    
    producto_final = df[df['CUM_COMPLETO'] == cum_a_actualizar]
    
    if producto_final.empty:
        print(f"⚠️ CUM COMPLETO '{cum_a_actualizar}' no encontrado en la lista. Cancelando.")
        return True
        
    idx = producto_final.index[0]
    
    # 6. Decidir qué valor guardar (GTIN o Limpieza)
    if gtin.upper() == 'BORRAR':
        valor_a_guardar = pd.NA
        confirmacion_msg = f"¿Confirmas que deseas BORRAR el GTIN de la fila {cum_a_actualizar}? (s/n): "
    else:
        valor_a_guardar = gtin
        confirmacion_msg = f"¿Guardar el GTIN {gtin} en ESTA fila? (s/n): "
        
    print(f"\n✨ Confirmación: Actualizando {producto_final['producto'].iloc[0]} (CUM: {cum_a_actualizar})")

    confirmacion = input(confirmacion_msg).lower().strip()
    
    if confirmacion == 's':
        df.loc[idx, 'GTIN_ASIGNADO'] = valor_a_guardar
        
        # Rellenar/Limpiar columnas auxiliares
        if valor_a_guardar is not pd.NA:
            df.loc[idx, 'NOMBRE_EXTRAIDO_GOOGLE'] = producto_final['producto'].iloc[0]
            df.loc[idx, 'SNIPPET_GOOGLE'] = 'Asignado manualmente'
        else:
            df.loc[idx, 'NOMBRE_EXTRAIDO_GOOGLE'] = pd.NA
            df.loc[idx, 'SNIPPET_GOOGLE'] = pd.NA

        print("✨ Datos actualizados en la memoria del programa.")
    else:
        print("🚫 Actualización cancelada.")
        
    time.sleep(0.5)
    return True

# --- FUNCIÓN PARA GUARDAR CSV ---
def guardar_csv(df):
    """Guarda todos los cambios en el archivo CSV (sobrescribe el original)."""
    # Excluimos la columna CUM_COMPLETO al guardar
    df_guardar = df.drop(columns=['CUM_COMPLETO'], errors='ignore') 
    df_guardar.to_csv(NOMBRE_ARCHIVO, index=False, encoding='utf-8') 
    print(f"\n💾 ¡TODOS LOS CAMBIOS SE HAN GUARDADO en '{NOMBRE_ARCHIVO}'!")

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    df_principal = cargar_csv()
    
    if df_principal is None:
        exit()
        
    print("--------------------------------------------------------------------------------")
    print("ASISTENTE DE ACTUALIZACIÓN DE MEDICAMENTOS (Método: GTIN + Búsqueda por Keyword)")
    print("--------------------------------------------------------------------------------")
    
    while True:
        if not buscar_y_actualizar_producto(df_principal):
            break
            
        guardar_ahora = input("¿Deseas guardar los cambios en el archivo CSV ahora? (s/n): ").lower().strip()
        if guardar_ahora == 's':
            guardar_csv(df_principal)
            
    # Guarda una última vez al salir del bucle
    guardar_csv(df_principal)
    print("¡Programa finalizado! Revisa tu archivo CSV actualizado.")