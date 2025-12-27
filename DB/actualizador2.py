import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# 1. Cargar CSV base
df = pd.read_csv("CÓDIGO_ÚNICO_DE_MEDICAMENTOS_VIGENTES_20250922.csv", dtype=str)
df["CUM_COMPLETO"] = df["expedientecum"] + "-" + df["consecutivocum"]

# 2. Función para buscar GTIN en Google
def buscar_gtin(cum):
    url = f"https://www.google.com/search?q={cum}+GTIN"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            texto = soup.get_text(" ")
            match = re.search(r"\b\d{13,14}\b", texto)  # GTIN suele tener 13 o 14 dígitos
            if match:
                return match.group(0)
    except Exception as e:
        print(f"Error con {cum}: {e}")
    return None

# 3. Aplicar a una muestra (por tiempo y para no bloquear IP)
df["GTIN_SCRAPING"] = df["CUM_COMPLETO"].head(20).apply(buscar_gtin)  # prueba con 20 primeros

# 4. Guardar resultados
df.to_csv("medicamentos_gtin_google.csv", index=False)
print("Archivo generado: medicamentos_gtin_google.csv")
