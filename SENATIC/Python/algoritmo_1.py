"""
Requerimiento 1: Cálculo del promedio de números pares en una lista.

Temas aplicados:
- Cálculos matemáticos y lógicos: Se calcula el promedio de números pares.
- Gestión de colecciones de datos: Se utiliza una lista para almacenar los números.
- Implementación de funciones: Se define una función para realizar el cálculo.
"""

def calcular_promedio_pares(lista_numeros):
    """
    Función que calcula el promedio de los números pares en una lista.

    Parámetros:
    lista_numeros (list): Lista de números enteros.

    Retorna:
    float: Promedio de los números pares.
    """
    # Filtrar los números pares de la lista
    numeros_pares = [num for num in lista_numeros if num % 2 == 0]

    # Verificar si hay números pares en la lista
    if len(numeros_pares) == 0:
        return 0  # Si no hay pares, el promedio es 0

    # Calcular el promedio de los números pares
    promedio = sum(numeros_pares) / len(numeros_pares)
    return promedio

# Lista de ejemplo
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Llamar a la función y mostrar el resultado
resultado = calcular_promedio_pares(numeros)
print(f"El promedio de los números pares es: {resultado}")

"""
Paso a paso del código:
1. Se define la función `calcular_promedio_pares` que recibe una lista de números.
2. Dentro de la función, se utiliza una comprensión de listas para filtrar los números pares.
   - Aquí se aplica la lógica matemática: `num % 2 == 0` verifica si un número es par.
3. Se verifica si la lista de números pares está vacía. Si está vacía, se retorna 0.
4. Si hay números pares, se calcula el promedio sumando los números pares y dividiendo entre la cantidad de pares.
5. Fuera de la función, se define una lista de ejemplo `numeros`.
6. Se llama a la función con la lista de ejemplo y se imprime el resultado.

Temas aplicados:
- **Cálculos matemáticos y lógicos**: El cálculo del promedio y la verificación de números pares.
- **Gestión de colecciones de datos**: Uso de listas para almacenar y filtrar datos.
- **Implementación de funciones**: La lógica está encapsulada en una función reutilizable.
"""