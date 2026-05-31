"""
Requerimiento 5: Resolver el problema de las Torres de Hanoi para n discos.

Temas aplicados:
- Cálculos matemáticos y lógicos: Determinar los movimientos necesarios para resolver el problema.
- Implementación de funciones y procedimientos: Uso de recursión para resolver el problema.
- Resolución de problemas: Combinación de estructuras de control y recursión para dividir el problema en subproblemas más pequeños.
"""

def torres_de_hanoi(n, origen, destino, auxiliar):
    """
    Función que resuelve el problema de las Torres de Hanoi para n discos.

    Parámetros:
    n (int): Número de discos.
    origen (str): Nombre de la torre de origen.
    destino (str): Nombre de la torre de destino.
    auxiliar (str): Nombre de la torre auxiliar.

    Retorna:
    None
    """
    if n == 1:
        # Caso base: mover un disco directamente de origen a destino
        print(f"Mover disco 1 de {origen} a {destino}")
        return

    # Mover n-1 discos de origen a auxiliar usando destino como torre auxiliar
    torres_de_hanoi(n-1, origen, auxiliar, destino)

    # Mover el disco más grande de origen a destino
    print(f"Mover disco {n} de {origen} a {destino}")

    # Mover los n-1 discos de auxiliar a destino usando origen como torre auxiliar
    torres_de_hanoi(n-1, auxiliar, destino, origen)

# Número de discos de ejemplo
num_discos = 3

# Llamar a la función y mostrar los movimientos
print(f"Resolviendo Torres de Hanoi para {num_discos} discos:")
torres_de_hanoi(num_discos, "Origen", "Destino", "Auxiliar")

"""
Paso a paso del código:
1. Se define la función `torres_de_hanoi` que recibe el número de discos y los nombres de las torres.
2. Si el número de discos es 1 (caso base), se imprime el movimiento directo del disco de la torre de origen a la de destino.
3. Si hay más de un disco, se divide el problema en tres pasos:
   - Mover n-1 discos de la torre de origen a la torre auxiliar.
   - Mover el disco más grande de la torre de origen a la torre de destino.
   - Mover los n-1 discos de la torre auxiliar a la torre de destino.
4. Fuera de la función, se define un número de discos de ejemplo `num_discos`.
5. Se llama a la función con los nombres de las torres y se imprimen los movimientos necesarios para resolver el problema.

Temas aplicados:
- **Cálculos matemáticos y lógicos**: Determinación de los movimientos necesarios para resolver el problema.
- **Implementación de funciones y procedimientos**: Uso de recursión para dividir el problema en subproblemas más pequeños.
- **Resolución de problemas**: Combinación de estructuras de control y recursión para resolver el problema de manera eficiente.
"""