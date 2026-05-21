import random
import secrets
import base64

# Constantes para representar el estado de una casilla
HIDDEN = -1
MINE = -2

# Clase para representar una casilla del tablero
class Tile:
    def __init__(self, value):
        self.value = value
        self.revealed = False
        self.flagged = False

    def __str__(self):
        if self.revealed:
            if self.value == MINE:
                return "*"
            elif self.value == 0:
                return " "
            else:
                return str(self.value)
        else:
            if self.flagged:
                return "F"
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

    @classmethod
    def from_mine_positions(cls, rows, cols, mine_positions):
        """Crea un Board directamente a partir de posiciones de minas (lista de (r,c))."""
        b = cls.__new__(cls)
        b.rows = rows
        b.cols = cols
        b.mines = len(mine_positions)
        b.board = [[Tile(HIDDEN) for _ in range(cols)] for _ in range(rows)]
        for (r, c) in mine_positions:
            if 0 <= r < rows and 0 <= c < cols:
                b.board[r][c].value = MINE
        b.calculate_values()
        return b

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
                nr, nc = row + i, col + j
                if not (0 <= nr < self.rows) or not (0 <= nc < self.cols):
                    continue
                if self.board[nr][nc].value == MINE:
                    count += 1
        return count

    def reveal_tile(self, row, col):
        """Revela una casilla.
        Devuelve:
            False -> se reveló una mina (pérdida)
            True  -> revelación normal (o nada si ya estaba revelada/flagged)
        """
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return True  # fuera de rango no hace nada aquí

        tile = self.board[row][col]

        if tile.flagged or tile.revealed:
            return True

        if tile.value == MINE:
            tile.revealed = True
            return False  # mina: pérdida

        # revelar recursivamente si es 0
        self._flood_reveal(row, col)
        return True

    def _flood_reveal(self, row, col):
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return
        tile = self.board[row][col]
        if tile.revealed or tile.flagged:
            return
        tile.revealed = True
        if tile.value == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    self._flood_reveal(row + i, col + j)

    def flag_tile(self, row, col):
        """Marca o desmarca una casilla (no puede marcarse si ya está revelada)."""
        if not (0 <= row < self.rows) or not (0 <= col < self.cols):
            return False
        tile = self.board[row][col]
        if tile.revealed:
            return False
        tile.flagged = not tile.flagged
        return True

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].value == MINE:
                    self.board[r][c].revealed = True

    def all_non_mine_revealed(self):
        return all(t.revealed or t.value == MINE for r in self.board for t in r)

    def mine_positions(self):
        """Devuelve una lista de tuplas (r, c) con las minas — útil para tests y debugging."""
        pos = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].value == MINE:
                    pos.append((r, c))
        return sorted(pos)

    def __str__(self):
        # Header with column indices
        s = "   " + " ".join(f"{c}" for c in range(self.cols)) + "\n"
        for r, row in enumerate(self.board):
            s += f"{r:2} " + " ".join(str(tile) for tile in row) + "\n"
        return s

# --- Seed encoding/decoding (reproducible and compact) ---
# Formato: seedv1:<base64_urlsafe(payload)>
# Payload = rows(2 bytes BE) | cols(2 bytes BE) | bitmask bytes (row-major, 1=mine)
def encode_board_seed(rows, cols, mine_positions):
    bitlen = rows * cols
    bits = ['0'] * bitlen
    for (r, c) in mine_positions:
        if 0 <= r < rows and 0 <= c < cols:
            bits[r * cols + c] = '1'
    bits_str = ''.join(bits) if bits else '0'
    bit_int = int(bits_str, 2) if bits_str else 0
    byte_len = (bitlen + 7) // 8
    bit_bytes = bit_int.to_bytes(byte_len, 'big') if byte_len > 0 else b''
    header = rows.to_bytes(2, 'big') + cols.to_bytes(2, 'big')
    payload = header + bit_bytes
    b64 = base64.urlsafe_b64encode(payload).decode('ascii').rstrip('=')
    return f"seedv1:{b64}"

def decode_board_seed(seed_str):
    """Devuelve (rows, cols, mine_positions) o lanza ValueError si inválido."""
    if not seed_str.startswith("seedv1:"):
        raise ValueError("Formato de seed desconocido")
    b64 = seed_str[len("seedv1:"):]
    # agregar padding
    padding = '=' * (-len(b64) % 4)
    payload = base64.urlsafe_b64decode(b64 + padding)
    if len(payload) < 4:
        raise ValueError("Payload de seed demasiado corto")
    rows = int.from_bytes(payload[0:2], 'big')
    cols = int.from_bytes(payload[2:4], 'big')
    bit_bytes = payload[4:]
    bitlen = rows * cols
    if bitlen == 0:
        return rows, cols, []
    bit_int = int.from_bytes(bit_bytes, 'big')
    bits_str = bin(bit_int)[2:].rjust((len(bit_bytes) * 8), '0')
    # bits_str puede tener más bits que bitlen (padding a la izquierda), cortar por la derecha:
    if len(bits_str) > bitlen:
        bits_str = bits_str[-bitlen:]
    mine_positions = []
    for idx, ch in enumerate(bits_str):
        if ch == '1':
            r = idx // cols
            c = idx % cols
            mine_positions.append((r, c))
    return rows, cols, sorted(mine_positions)

# Parsing helper (sin cambios funcionales del CLI)
def parse_command(text):
    text = text.strip().lower()
    if not text:
        return None
    if text in ('q', 'quit', 'exit'):
        return ('quit',)
    if text in ('help', 'h', '?'):
        return ('help',)
    if text.startswith('seed '):
        parts = text.split()
        if len(parts) >= 2:
            return ('seed', parts[1])
        return None

    # detect flag command
    if text.startswith('f') and len(text) > 1 and not text[1].isdigit():
        parts = text.split(maxsplit=1)
        if len(parts) == 1:
            return None
        rest = parts[1]
        coords = _parse_coords(rest)
        if coords:
            r, c = coords
            return ('flag', r, c)
        return None
    if text.startswith('flag '):
        parts = text.split(maxsplit=1)
        if len(parts) == 2:
            coords = _parse_coords(parts[1])
            if coords:
                return ('flag', coords[0], coords[1])
        return None

    coords = _parse_coords(text)
    if coords:
        return ('reveal', coords[0], coords[1])

    if text.startswith('f') and len(text) > 1:
        coords = _parse_coords(text[1:])
        if coords:
            return ('flag', coords[0], coords[1])

    return None

def _parse_coords(s):
    s = s.strip()
    s = s.replace(',', ' ')
    parts = s.split()
    if len(parts) < 2:
        return None
    if parts[0].lstrip('-').isdigit() and parts[1].lstrip('-').isdigit():
        r = int(parts[0])
        c = int(parts[1])
        return (r, c)
    return None

# Función para jugar una partida del buscaminas
def play_game():
    print("Buscaminas (modo consola). Escribe 'help' para ver comandos.")
    seed_input = input("Ingresa la semilla (opcional, deja vacío para aleatorio). Puedes pegar 'seedv1:...' para reconstruir tablero: ").strip()

    seed_provided = False
    canonical_seed = None
    board = None

    # Si el usuario pega una seed codificada (seedv1:...), decodificamos y construimos el tablero directamente
    if seed_input.startswith("seedv1:"):
        try:
            rows, cols, mine_positions = decode_board_seed(seed_input)
            board = Board.from_mine_positions(rows, cols, mine_positions)
            seed_provided = True
            canonical_seed = seed_input
            print("Seed codificada detectada: reconstruido tablero desde la semilla.")
        except Exception as e:
            print("Seed codificada inválida:", e)
            return

    else:
        # Si es un número entero, lo usamos como semilla para random (compatibilidad con comportamiento anterior)
        if seed_input:
            try:
                seed_val = int(seed_input)
                random.seed(seed_val)
                seed_provided = True
                print(f"Semilla numérica fijada a {seed_val}. Tablero reproducible (formato canónico disponible al terminar).")
            except ValueError:
                print("Semilla no reconocida; se usará aleatorio.")

        # Pedimos dimensiones y minas (si no reconstruimos desde seedv1)
        try:
            rows = int(input("Ingresa el número de filas: "))
            cols = int(input("Ingresa el número de columnas: "))
            mines = int(input("Ingresa el número de minas: "))
        except ValueError:
            print("Entrada inválida. Usa números enteros.")
            return

        if rows <= 0 or cols <= 0:
            print("Filas y columnas deben ser mayores que 0.")
            return
        if mines < 0 or mines >= rows * cols:
            print("Número de minas inválido.")
            return

        # Crear tablero mediante random (si seed numérica fue fijada arriba, será reproducible)
        board = Board(rows, cols, mines)
        # Generar la seed canónica basada en la posición de minas del tablero actual
        canonical_seed = encode_board_seed(board.rows, board.cols, board.mine_positions())

    print("Comandos: 'r,c' para revelar, 'f r,c' para marcar/desmarcar, 'seedv1:...' para reconstruir tablero exacto, 'seed N' para cambiar semilla (no reinicia tablero), 'help', 'q' para salir.")
    game_over = False
    while True:
        print(board)
        user = input("Ingresa comando (ej: '1,2' o 'f 1,2'): ")
        cmd = parse_command(user)
        if cmd is None:
            print("Comando inválido. Escribe 'help' para ver comandos.")
            continue
        if cmd[0] == 'quit':
            print("Saliendo...")
            break
        if cmd[0] == 'help':
            print("Comandos disponibles:")
            print("  fila,col   -> revelar casilla")
            print("  f fila,col -> marcar/desmarcar casilla (flag)")
            print("  seed N     -> fijar semilla numérica para reproducibilidad (no reinicia tablero actual)")
            print("  seedv1:... -> formato canónico para reconstruir exactamente el tablero (pegar para reproducir)")
            print("  q          -> salir")
            continue
        if cmd[0] == 'seed':
            # aquí 'seed' lleva un string en lugar de int: si es 'seedv1:...' podemos reconstruir,
            # si es numérico, seteamos random para futuras operaciones
            arg = cmd[1]
            if arg.startswith("seedv1:"):
                try:
                    rows2, cols2, mine_positions = decode_board_seed(arg)
                    board = Board.from_mine_positions(rows2, cols2, mine_positions)
                    canonical_seed = arg
                    print("Tablero reconstruido desde seed canónica.")
                except Exception as e:
                    print("Seed canónica inválida:", e)
            else:
                try:
                    sval = int(arg)
                    random.seed(sval)
                    print(f"Semilla numérica fijada a {sval}. (Nota: no reinicia el tablero actual.)")
                except ValueError:
                    print("Valor de seed inválido.")
            continue

        action, r, c = cmd
        if not (0 <= r < board.rows) or not (0 <= c < board.cols):
            print("Coordenadas fuera de rango.")
            continue
        if action == 'flag':
            ok = board.flag_tile(r, c)
            if not ok:
                print("No se puede marcar esa casilla (quizá ya revelada).")
            continue
        if action == 'reveal':
            result = board.reveal_tile(r, c)
            if result is False:
                board.reveal_all_mines()
                print(board)
                print("¡Has perdido!")
                game_over = True
                break
            if board.all_non_mine_revealed():
                print(board)
                print("¡Has ganado!")
                game_over = True
                break

    # Mostrar la semilla canónica al finalizar (si existe): este formato codifica filas/columnas/posiciones exactamente.
    if canonical_seed:
        if seed_provided:
            print(f"Semilla canónica (reproducible exactamente): {canonical_seed} (también se puede compartir para reconstruir este tablero).")
        else:
            print(f"Semilla generada y usada (canónica, reproduce exactamente este tablero): {canonical_seed}")
    else:
        print("No se generó semilla canónica para este juego.")

if __name__ == "__main__":
    play_game()