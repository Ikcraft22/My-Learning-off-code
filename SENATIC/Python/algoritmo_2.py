"""
Requerimiento 2: Verificar si una palabra es un palíndromo.

Temas aplicados:
- Manipulación de cadenas de texto: Se invierte la cadena y se compara con la original.
- Implementación de funciones: Se define una función para realizar la verificación.
- Resolución de problemas: Se combinan estructuras de control para verificar la condición.
"""

def es_palindromo(palabra):
    """
    Función que verifica si una palabra es un palíndromo.

    Parámetros:
    palabra (str): Palabra a verificar.

    Retorna:
    bool: True si es un palíndromo, False en caso contrario.
    """
    # Convertir la palabra a minúsculas para evitar problemas de mayúsculas/minúsculas
    palabra = palabra.lower()

    # Invertir la palabra
    palabra_invertida = palabra[::-1]

    # Verificar si la palabra original es igual a la invertida
    return palabra == palabra_invertida

# Palabra de ejemplo
palabra = "Anilina"

# Llamar a la función y mostrar el resultado
if es_palindromo(palabra):
    print(f"La palabra '{palabra}' es un palíndromo.")
else:
    print(f"La palabra '{palabra}' no es un palíndromo.")

"""
Paso a paso del código:
1. Se define la función `es_palindromo` que recibe una palabra como parámetro.
2. Dentro de la función, se convierte la palabra a minúsculas usando `lower()` para evitar problemas de comparación.
3. Se invierte la palabra utilizando slicing (`[::-1]`).
4. Se compara la palabra original con la invertida. Si son iguales, la palabra es un palíndromo.
5. Fuera de la función, se define una palabra de ejemplo `palabra`.
6. Se llama a la función con la palabra de ejemplo y se imprime si es o no un palíndromo.

Temas aplicados:
- **Manipulación de cadenas de texto**: Conversión a minúsculas e inversión de la cadena.
- **Implementación de funciones**: La lógica está encapsulada en una función reutilizable.
- **Resolución de problemas**: Uso de estructuras de control (`if`) para determinar el resultado.
"""