import argparse
import os
import urllib.request

# Crea un analizador de argumentos para procesar la línea de comandos
parser = argparse.ArgumentParser(description='Descargador de videos')

# Agrega un argumento para especificar la URL del video
parser.add_argument('url', help='URL del video a descargar')

# Agrega un argumento opcional para especificar la calidad del video
parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high'],
                    help='calidad del video (baja, media o alta)')

# Agrega un argumento opcional para especificar el nombre del archivo de salida
parser.add_argument('-o', '--output',
                    help='nombre del archivo de salida')

# Procesa los argumentos de la línea de comandos
args = parser.parse_args()

# Obtiene la URL del video y la calidad deseada
url = args.url
quality = args.quality

# Si no se especificó un nombre de archivo de salida, utiliza el nombre del archivo del video original
if args.output:
    local_filename = args.output
else:
    local_filename = url.split('/')[-1]

# Si se especificó una calidad, agrega un indicador de calidad al nombre del archivo
if quality:
    local_filename = f'{quality}_{local_filename}'

# Descarga el contenido del video y lo guarda en el archivo local
urllib.request.urlretrieve(url, local_filename)

print(f'Descarga completa: {local_filename}')
