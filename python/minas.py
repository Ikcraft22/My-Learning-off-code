import random

# Constantes para representar el estado de una casilla
HIDDEN = -1
MINE = -2

# Clase para representar una casilla del tablero
class Tile:
    def __init__(self, value):
        self.value = value
        self.revealed = False

    def __str__(self):
        if self.revealed:
            if self.value == MINE:
                return "*"
            elif self.value == 0:
                return " "
            else:
                return str(self.value)
        else:
            return "X"

# Clase para representar el tablero del juego
class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        # Crear el tablero con todas las casillas ocultas
        self.board = [[Tile(HIDDEN) for _ in range(cols)] for _ in range(rows)]

        # Colocar las minas en posiciones aleatorias
        self.place_mines()

        # Calcular los valores de las casillas que no son minas
        self.calculate_values()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col].value != MINE:
                self.board[row][col].value = MINE
                mines_placed += 1

    def calculate_values(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col].value != MINE:
                    self.board[row][col].value = self.count_adjacent_mines(row, col)

    def count_adjacent_mines(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if not (0 <= row + i < self.rows) or not (0 <= col + j < self.cols):
                    continue
                if self.board[row + i][col + j].value == MINE:
                    count += 1
        return count

    def __str__(self):
        s = ""
        for row in self.board:
            for tile in row:
                s += str(tile)
            s += "\n"
        return s

# Función para jugar una partida del buscaminas
def play_game():
    rows = int(input("Ingresa el número de filas: "))
    cols = int(input("Ingresa el número de columnas: "))
    mines = int(input("Ingresa el número de minas: "))
    board = Board(rows, cols, mines)
while True:
    print(Board)
    row = int(input("Ingresa la fila: "))
    col = int(input("Ingresa la columna: "))
    if Board.board[row][col].value == MINE:
        print("¡Has perdido!")
        break
    Board.board[row][col].revealed = True
    if all(tile.revealed or tile.value == MINE for row in Board.board for tile in row):
        print("¡Has ganado!")
        break

