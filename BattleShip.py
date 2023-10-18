import random
from colorama import Fore, Style

def build_game_board(board):
    for _ in range(20):
        board.append(["O"] * 20)

def print_game_boards(board1, board2, shots1, shots2):
    max_row_width = len(str(len(board1) - 1))

    # Imprime las coordenadas en la parte superior de ambos tableros
    print(" " * (max_row_width + 1), end="")
    for i in range(20):
        print(f"{i:2}", end=" ")
    print("    ", end="")
    for i in range(20):
        print(f"{i:2}", end=" ")
    print()

    # Imprime los tableros con las coordenadas en los extremos
    for i, (row1, row2) in enumerate(zip(board1, board2)):
        print(f"{i:>{max_row_width}} ", end="")
        for cell in row1:
            if cell == "Y":
                print(Fore.BLUE + cell + Style.RESET_ALL, end=" ")
            elif cell == "X":
                print(Fore.RED + cell + Style.RESET_ALL, end=" ")
            else:
                print(cell, end=" ")
        print("    ", end="")
        for cell in row2:
            if cell == "Y":
                print(Fore.BLUE + cell + Style.RESET_ALL, end=" ")
            elif cell == "X":
                print(Fore.RED + cell + Style.RESET_ALL, end=" ")
            else:
                print(cell, end=" ")
        print()

    # Imprime los disparos de los jugadores en tiempo real
    print("\nDisparos Jugador 1:")
    for shot in shots1:
        row, col = shot
        print(f"Jugador 1 disparó en ({row}, {col})")
    print("\nDisparos Jugador 2:")
    for shot in shots2:
        row, col = shot
        print(f"Jugador 2 disparó en ({row}, {col})")

def place_ships(board):
    ship_sizes = [3, 2, 1]

    for size in ship_sizes:
        place_ship(board, size, Fore.BLUE + "Y" + Style.RESET_ALL)

def place_ship(board, size, symbol):
    while True:
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        orientation = random.choice(["horizontal", "vertical"])

        if orientation == "horizontal":
            if can_place_ship_horizontally(board, row, col, size):
                for i in range(size):
                    board[row][col + i] = symbol
                break
        else:
            if can_place_ship_vertically(board, row, col, size):
                for i in range(size):
                    board[row + i][col] = symbol
                break

def can_place_ship_horizontally(board, row, col, size):
    if col + size > len(board[0]):
        return False
    for i in range(size):
        if board[row][col + i] != "O":
            return False
    return True

def can_place_ship_vertically(board, row, col, size):
    if row + size > len(board):
        return False
    for i in range(size):
        if board[row + i][col] != "O":
            return False
    return True

def check_victory(board):
    verdad = True
    for i in range(20):
        for k  in range(20):
            if(board[i][k]==Fore.BLUE + "Y" + Style.RESET_ALL):
                verdad = False
    return verdad

def bot_player(board, shots):
    while True:
        row2 = random.randint(0, 19)
        col2 = random.randint(0, 19)
        if (row2, col2) not in shots:
            return row2, col2

def main():
    game_board1 = []
    game_board2 = []
    build_game_board(game_board1)
    build_game_board(game_board2)
    place_ships(game_board1)
    place_ships(game_board2)

    print("¡Bienvenidos al juego de Batalla Naval!")

    shots1 = []  # Lista de disparos del Jugador 1
    shots2 = []  # Lista de disparos del Jugador 2

    while True:
        print_game_boards(game_board1, game_board2, shots1, shots2)
        try:
            row1 = int(input("Jugador 1: Ingresa la fila para tu ataque (0-19): "))
            col1 = int(input("Jugador 1: Ingresa la columna para tu ataque (0-19): "))

            if (
                0 <= row1 < 20
                and 0 <= col1 < 20
            ):
                if game_board1[row1][col1] == "Y":
                    print("¡Jugador 1 ha golpeado un barco!")
                    game_board1[row1][col1] = Fore.RED + "X" + Style.RESET_ALL
                else:
                    print("¡Jugador 1 ha fallado!")
                    game_board1[row1][col1] = Fore.GREEN + "X" + Style.RESET_ALL

                shots1.append((row1, col1))

                if check_victory(game_board1):
                    print("Jugador 1 gana. ¡Felicidades!")
                    break

            else:
                print("Coordenadas fuera de rango. Deben estar entre 0 y 19.")
        except ValueError:
            print("Entrada no válida. Ingresa un número entre 0 y 19.")

        print_game_boards(game_board1, game_board2, shots1, shots2)

         # Turno del bot (Jugador 2)
        row2, col2 = bot_player(game_board2, shots2)

        if game_board2[row2][col2] == "Y":
            print("¡Jugador 2 ha golpeado un barco!")
            game_board2[row2][col2] = Fore.RED + "X" + Style.RESET_ALL
        else:
            print("¡Jugador 2 ha fallado!")
            game_board2[row2][col2] = Fore.GREEN + "X" + Style.RESET_ALL

        shots2.append((row2, col2))

        if check_victory(game_board2):
            print("Jugador 2 (bot) gana. ¡Felicidades!")
            break
        print_game_boards(game_board1, game_board2, shots1, shots2)

if __name__ == "__main__":
    main()

    {
  "action": "c", # connection, attack, lose, build, disconnect, select
  "bot": 0, # 0 o 1, 1: partida vs bot, 0: partida vs otro cliente

  "ships": {
            "p": [], # cordenada (x,y) y orientación (0: vertical, 1: horizontal)
            "b": [],
            "s": []
           },
  "position": [], # posicion de ataque
}