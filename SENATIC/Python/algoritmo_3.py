"""
Requerimiento 3: Ordenar una lista de diccionarios por un valor específico.

Temas aplicados:
- Gestión de colecciones de datos: Se utiliza una lista de diccionarios.
- Implementación de funciones: Se define una función para realizar la ordenación.
- Resolución de problemas: Se combinan estructuras de control para manejar casos especiales.
"""

def ordenar_diccionarios(lista_diccionarios, clave):
    """
    Función que ordena una lista de diccionarios por un valor específico.

    Parámetros:
    lista_diccionarios (list): Lista de diccionarios a ordenar.
    clave (str): Clave por la cual ordenar los diccionarios.

    Retorna:
    list: Lista de diccionarios ordenada.
    """
    # Verificar si la lista está vacía
    if not lista_diccionarios:
        print("La lista está vacía.")
        return []

    # Verificar si la clave existe en los diccionarios
    if not all(clave in diccionario for diccionario in lista_diccionarios):
        print(f"La clave '{clave}' no existe en todos los diccionarios.")
        return []

    # Ordenar la lista de diccionarios por la clave especificada
    lista_ordenada = sorted(lista_diccionarios, key=lambda diccionario: diccionario[clave])
    return lista_ordenada

# Lista de ejemplo
personas = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Luis", "edad": 30},
    {"nombre": "Carlos", "edad": 20}
]

# Llamar a la función y mostrar el resultado
clave_orden = "edad"
resultado = ordenar_diccionarios(personas, clave_orden)
print(f"Lista ordenada por '{clave_orden}': {resultado}")

"""
Paso a paso del código:
1. Se define la función `ordenar_diccionarios` que recibe una lista de diccionarios y una clave para ordenar.
2. Se verifica si la lista está vacía. Si está vacía, se retorna una lista vacía.
3. Se verifica si la clave existe en todos los diccionarios de la lista. Si no existe, se retorna una lista vacía.
4. Se utiliza la función `sorted` con una función lambda para ordenar los diccionarios por el valor de la clave especificada.
5. Fuera de la función, se define una lista de diccionarios de ejemplo `personas`.
6. Se llama a la función con la lista de ejemplo y la clave de ordenación, y se imprime el resultado.

Temas aplicados:
- **Gestión de colecciones de datos**: Uso de listas y diccionarios para almacenar y manipular datos.
- **Implementación de funciones**: La lógica está encapsulada en una función reutilizable.
- **Resolución de problemas**: Uso de estructuras de control (`if`) para manejar casos especiales.
"""