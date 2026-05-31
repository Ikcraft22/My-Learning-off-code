"""
Requerimiento 4: Generar una secuencia de Fibonacci hasta un número dado.

Temas aplicados:
- Cálculos matemáticos y lógicos: Generación de la secuencia de Fibonacci.
- Implementación de funciones: Se define una función para generar la secuencia.
- Resolución de problemas: Uso de estructuras de control para manejar la lógica iterativa.
"""

def generar_fibonacci(hasta):
    """
    Función que genera la secuencia de Fibonacci hasta un número dado.

    Parámetros:
    hasta (int): Límite superior para la secuencia de Fibonacci.

    Retorna:
    list: Secuencia de Fibonacci generada.
    """
    # Inicializar la secuencia con los dos primeros números
    secuencia = [0, 1]

    # Generar la secuencia hasta el límite especificado
    while True:
        siguiente = secuencia[-1] + secuencia[-2]  # Suma de los dos últimos números
        if siguiente > hasta:
            break  # Salir del bucle si se supera el límite
        secuencia.append(siguiente)

    return secuencia

# Límite superior de ejemplo
limite = 100

# Llamar a la función y mostrar el resultado
resultado = generar_fibonacci(limite)
print(f"Secuencia de Fibonacci hasta {limite}: {resultado}")

"""
Paso a paso del código:
1. Se define la función `generar_fibonacci` que recibe un límite superior como parámetro.
2. Se inicializa la secuencia con los dos primeros números de Fibonacci: 0 y 1.
3. Se utiliza un bucle `while` para generar los siguientes números de la secuencia.
   - En cada iteración, se calcula el siguiente número como la suma de los dos últimos números de la secuencia.
   - Si el siguiente número supera el límite, se rompe el bucle.
4. Fuera de la función, se define un límite superior de ejemplo `limite`.
5. Se llama a la función con el límite y se imprime la secuencia generada.

Temas aplicados:
- **Cálculos matemáticos y lógicos**: Generación de números de Fibonacci mediante suma.
- **Implementación de funciones**: La lógica está encapsulada en una función reutilizable.
- **Resolución de problemas**: Uso de un bucle `while` para manejar la lógica iterativa.
"""