def pedir_entero(mensaje, minimo=0, maximo=9):
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():
            numero = int(entrada)
            if minimo <= numero <= maximo:
                return numero
            else:
                print(f"Por favor, ingresa un número entre {minimo} y {maximo}.")
        else:
            print("Entrada inválida. Debes ingresar un número entero.")

def pedir_direccion():
    while True:
        direccion = input("Dirección (H para horizontal, V para vertical): ").upper()
        if direccion in ['H', 'V']:
            return direccion
        else:
            print("Entrada inválida. Debes ingresar 'H' o 'V'.")

class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.positions = []
        self.hits = 0

    def place_ship(self, start_row, start_col, direction, board):
        positions = []
        if direction == 'H':
            if start_col + self.size > len(board[0]):
                return False
            for i in range(self.size):
                if board[start_row][start_col + i] != ' ':
                    return False
                positions.append((start_row, start_col + i))
        elif direction == 'V':
            if start_row + self.size > len(board):
                return False
            for i in range(self.size):
                if board[start_row + i][start_col] != ' ':
                    return False
                positions.append((start_row + i, start_col))
        else:
            return False
        
        for pos in positions:
            board[pos[0]][pos[1]] = self.name[0]
        self.positions = positions
        return True

    def hit(self):
        self.hits += 1
        return self.hits == self.size

class Destroyer(Ship):
    def __init__(self):
        super().__init__('Destructor', 2)

class Submarine(Ship):
    def __init__(self):
        super().__init__('Submarino', 3)

class Battleship(Ship):
    def __init__(self):
        super().__init__('Acorazado', 4)

class Player:
    def __init__(self, name):
        self.name = name
        self.board = [[' ' for _ in range(10)] for _ in range(10)]
        self.ships = []
        self.hits = [[' ' for _ in range(10)] for _ in range(10)]

    def place_ships(self):
        ships = [Destroyer(), Submarine(), Battleship()]
        for ship in ships:
            while True:
                print(f"{self.name}, coloca tu {ship.name} de tamaño {ship.size}.")
                start_row = pedir_entero("Fila inicial (0-9): ")
                start_col = pedir_entero("Columna inicial (0-9): ")
                direction = pedir_direccion()
                if ship.place_ship(start_row, start_col, direction, self.board):
                    self.ships.append(ship)
                    self.print_board(self.board)
                    break
                else:
                    print("Posición no válida. Inténtalo de nuevo.")

    def print_board(self, board):
        for row in board:
            print(" ".join(row))
        print()

    def attack(self, opponent):
        while True:
            print(f"{self.name}, elige una posición para atacar.")
            row = pedir_entero("Fila (0-9): ")
            col = pedir_entero("Columna (0-9): ")
            if 0 <= row < 10 and 0 <= col < 10:
                if opponent.board[row][col] == ' ':
                    print("Agua!")
                    self.hits[row][col] = 'A'
                    opponent.board[row][col] = 'A'
                    break
                elif opponent.board[row][col] != 'A':
                    print("Impacto!")
                    self.hits[row][col] = 'T'
                    for ship in opponent.ships:
                        if (row, col) in ship.positions:
                            if ship.hit():
                                print(f"¡Hundido! Has hundido el {ship.name}.")
                            break
                    opponent.board[row][col] = 'T'
                    break
                else:
                    print("Ya has atacado esta posición. Intenta de nuevo.")
            else:
                print("Posición no válida. Intenta de nuevo.")

    def all_ships_sunk(self):
        return all(ship.hits == ship.size for ship in self.ships)

class BattleshipGame:
    def __init__(self):
        self.player1 = Player("Jugador 1")
        self.player2 = Player("Jugador 2")

    def play(self):
        print("Bienvenido al juego de Batalla Naval!")
        print("Jugador 1 coloca sus barcos.")
        self.player1.place_ships()
        print("Jugador 2 coloca sus barcos.")
        self.player2.place_ships()

        current_player = self.player1
        opponent = self.player2

        while True:
            current_player.attack(opponent)
            if opponent.all_ships_sunk():
                print(f"¡{current_player.name} ha ganado el juego!")
                break
            current_player, opponent = opponent, current_player


game = BattleshipGame()

game.play()
