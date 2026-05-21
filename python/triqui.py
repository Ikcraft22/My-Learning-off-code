board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

def print_board():
  print('   1  2  3')
  for i in range(3):
    print(f"{i+1}  {board[i][0]}  {board[i][1]}  {board[i][2]}")

def check_win(player):
  # Verificar filas
  for i in range(3):
    if board[i][0] == player and board[i][1] == player and board[i][2] == player:
      return True
  # Verificar columnas
  for i in range(3):
    if board[0][i] == player and board[1][i] == player and board[2][i] == player:
      return True
  # Verificar diagonales
  if board[0][0] == player and board[1][1] == player and board[2][2] == player:
    return True
  if board[0][2] == player and board[1][1] == player and board[2][0] == player:
    return True
  return False

def check_draw():
  for i in range(3):
    for j in range(3):
      if board[i][j] == ' ':
        return False
  return True

current_player = 'X'
while True:
  print_board()
  row = int(input("Ingresa la fila (1, 2, 3): "))
  col = int(input("Ingresa la columna (1, 2, 3): "))
  if row < 1 or row > 3 or col < 1 or col > 3:
    print("Posición inválida. Intenta de nuevo.")
    continue
  if board[row-1][col-1] != ' ':
    print("Esa posición ya está ocupada. Intenta de nuevo.")
    continue
  board[row-1][col-1] = current_player
  if check_win(current_player):
    print_board()
    print(f"¡{current_player} ha ganado!")
    break
  if check_draw():
    print_board()
    print("¡Empate!")
    break
  if current_player == 'X':
    current_player = 'O'
  else:
    current_player = 'X'
