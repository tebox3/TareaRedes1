import socket
import json
import random
from colorama import Fore, Style
import time

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

def build_game_board(board):
    for _ in range(5):
        board.append(["O"] * 5)

def print_game_boards(board1, board2, shots1, shots2):
    max_row_width = len(str(len(board1) - 1))

    # Imprime las coordenadas en la parte superior de ambos tableros
    print(" " * (max_row_width + 1), end="")
    for i in range(5):
        print(f"{i:2}", end=" ")
    print("    ", end="")
    for i in range(5):
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
""" 
def place_ships(board,bot):
    place_ship(board, 3, Fore.BLUE + "Y" + Style.RESET_ALL,bot["p"]) #3 casillas
    place_ship(board, 2, Fore.BLUE + "Y" + Style.RESET_ALL,bot["b"]) #2 casillas
    place_ship(board, 1, Fore.BLUE + "Y" + Style.RESET_ALL,bot["s"]) #1 casillas """

def place_ships(board):
    ship_sizes = [3, 2, 1]

    for size in ship_sizes:
        place_ship1(board, size, Fore.BLUE + "Y" + Style.RESET_ALL)

def place_ship1(board, size, symbol):
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

def place_ship(board, size, symbol,bot):
    while True:
        """ row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        orientation = random.choice(["horizontal", "vertical"]) """

        row = bot[0]
        col = bot[1]

        if bot[2] == 0:
            orientation = "vertical"

        if bot[2] == 1:
            orientation = "horizontal"

        if orientation == "horizontal":
            if can_place_ship_horizontally(board, row, col, size):
                for i in range(size):
                    board[row][col + i] = symbol
                break
            else:
                print(row, col)
                print("Mal puesto!1")
                break
        else:
            if can_place_ship_vertically(board, row, col, size):
                for i in range(size):
                    board[row + i][col] = symbol
                break
            else:
                print(row, col)
                print("Mal puesto!2")
                break

""" def place_ship(board, size, symbol):
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
                break """

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
    for i in range(5):
        for k  in range(5):
            if(board[i][k]==Fore.BLUE + "Y" + Style.RESET_ALL):
                verdad = False
    return verdad

def bot_player(board, shots):
    while True:
        row2 = random.randint(0, 4) 
        col2 = random.randint(0, 4)
        if (row2, col2) not in shots:
            return row2, col2

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0].decode()
    address = bytesAddressPair[1]
    print("Mensaje recibido.")
    print("0 = ", bytesAddressPair[0].decode())
    print("1 = ", bytesAddressPair[1])
    try:
        # Intenta deserializar el mensaje JSON
        received_data = json.loads(message)

        # Verifica los campos del JSON uno por uno
        if "action" in received_data:
            action = received_data["action"]
            print("Received action:", action)
            if action == "c":
                status = 1  # Cambia esto según la lógica de tu aplicación
                # Aquí puedes realizar la verificación de la acción y establecer el valor de "status"
                # Por ejemplo, puedes verificar si la acción es válida y establecer "status" en 1 (True)
                # o en 0 (False) si es incorrecta.

                # Crear una respuesta JSON
                response_data = {
                    "action": action,
                    "status": status,
                    "position": []  # Establece las coordenadas jugadas por el usuario
                }

                # Serializar la respuesta como cadena JSON
                response_message = json.dumps(response_data)

                # Enviar la respuesta al cliente
                UDPServerSocket.sendto(str.encode(response_message), address)
                res1 = UDPServerSocket.recvfrom(bufferSize)
                message1 = res1[0].decode()
                address1 = res1[1]
                received_data1 = json.loads(message1)
                if "action" in received_data1 and "bot" in received_data1:
                    action1 = received_data1["action"]
                    bot1 = received_data1["bot"]
                    print("Received action1:", action1)
                    if action1 == "s" and bot1 == 0:
                        status = 1
                        response_data1 = {
                        "action": action1,
                        "status": status,
                        "position": []  # Establece las coordenadas jugadas por el usuario
                        }
                        # Enviar la respuesta al cliente
                        response_message1 = json.dumps(response_data1)
                        UDPServerSocket.sendto(str.encode(response_message1), address1)
                        time.sleep(2)
                        PedirBarquitos = {
                        "action": "b",
                        "status": 1,
                        "position": []  # Establece las coordenadas jugadas por el usuario
                        }
                        PedirBarquitos1 = json.dumps(PedirBarquitos)
                        UDPServerSocket.sendto(str.encode(PedirBarquitos1), address1)
                        #   Espera respuesta con posiciones barcos
                        res2 = UDPServerSocket.recvfrom(bufferSize)
                        message2 = res2[0].decode()
                        address2 = res2[1]
                        received_data2 = json.loads(message2)
                        if "action" in received_data2 and "bot" in received_data2 and "ships" in received_data2:
                            print("Barcos recibidos, json: ")
                            print(json.dumps(received_data2, indent=4))
                            action2 = received_data2["action"]
                            bot2 = received_data2["bot"]
                            ships2 = received_data2["ships"]
                            if action2 == "b" and bot2 == "":
                                try:
                                        print("1")
                                        game_board1 = []
                                        game_board2 = []
                                        print("2")
                                        #game_board2 = []
                                        build_game_board(game_board1)
                                        build_game_board(game_board2)
                                        shots1 = []  # Lista de disparos del Jugador 1
                                        shots2 = []  # Lista de disparos del Jugador 2
                                        print("3")
                                        #build_game_board(game_board2)
                                        #place_ships(game_board1,bot2)
                                        #place_ships(game_board2)
                                        place_ship(game_board1, 3, Fore.BLUE + "Y" + Style.RESET_ALL,ships2["p"]) #3 casillas
                                        print("4")
                                        for row in game_board1:
                                            print(" ".join(row))
                                        place_ship(game_board1, 2, Fore.BLUE + "Y" + Style.RESET_ALL,ships2["b"]) #2 casillas
                                        place_ship(game_board1, 1, Fore.BLUE + "Y" + Style.RESET_ALL,ships2["s"]) #1 casillas
                                        print("5")
                                        place_ships(game_board2)
                                        print("Tablero del jugador 1")
                                        for row in game_board1:
                                            print(" ".join(row))
                                        print("Tablero del jugador BOT")
                                        for row in game_board2:
                                            print(" ".join(row))
                                except Exception as error:
                                    print("El arreglo de barcos entregado por el cliente es incorrecto", error)
                                try:
                                    turnoActual = {
                                        "action": "t",
                                        "status": 1,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    turnoEnemigo = {
                                        "action": "t",
                                        "status": 0,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    acertado = {
                                        "action": "a",
                                        "status": 1,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    errado = {
                                        "action": "a",
                                        "status": 0,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    gano = {
                                        "action": "w",
                                        "status": 1,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    perdio = {
                                        "action": "l",
                                        "status": 1,
                                        "position": []  # Establece las coordenadas jugadas por el usuario
                                    }
                                    while True:
                                        turnoAc = json.dumps(turnoActual)
                                        UDPServerSocket.sendto(str.encode(turnoAc), address1)
                                        print_game_boards(game_board1, game_board2, shots1, shots2)
                                        try:
                                            ataque = UDPServerSocket.recvfrom(bufferSize)
                                            ataque1 = ataque[0].decode()
                                            ataque2 = json.loads(ataque1)
                                            if "action" in ataque2 and "position" in ataque2:
                                                if ataque2["action"] == "a":
                                                    row1 = ataque2["position"][1]
                                                    col1 = ataque2["position"][0]
                                            """ row1 = int(input("Jugador 1: Ingresa la fila para tu ataque (0-19): "))
                                            col1 = int(input("Jugador 1: Ingresa la columna para tu ataque (0-19): ")) """

                                            if ( 
                                                0 <= row1 < 5 
                                                and 0 <= col1 < 5
                                            ):
                                                if game_board1[row1][col1] == "Y":
                                                    print("¡Jugador 1 ha golpeado un barco!")
                                                    game_board1[row1][col1] = Fore.RED + "X" + Style.RESET_ALL
                                                    acertado1 = json.dumps(acertado)
                                                    UDPServerSocket.sendto(str.encode(acertado1, address1))
                                                else:
                                                    print("¡Jugador 1 ha fallado!")
                                                    game_board1[row1][col1] = Fore.GREEN + "X" + Style.RESET_ALL
                                                    errado1 = json.dumps(errado)
                                                    UDPServerSocket.sendto(str.encode(errado1, address1))
                                                shots1.append((row1, col1))

                                                if check_victory(game_board1):
                                                    print("Jugador 1 gana. ¡Felicidades!")
                                                    gano1 = json.dumps(gano)
                                                    UDPServerSocket.sendto(str.encode(gano1, address1))
                                                    break

                                            else:
                                                print("Coordenadas fuera de rango. Deben estar entre 0 y 19.")
                                        except ValueError:
                                            print("Entrada no válida. Ingresa un número entre 0 y 19.")

                                        print_game_boards(game_board1, game_board2, shots1, shots2)

                                        # Turno del bot (Jugador 2)
                                        row2, col2 = bot_player(game_board2, shots2)
                                        turnoEn = json.dumps(turnoEnemigo)
                                        UDPServerSocket.sendto(str.encode(turnoEn), address1)
                                        if game_board2[row2][col2] == "Y":
                                            print("¡Jugador 2 ha golpeado un barco!")
                                            acertado1 = json.dumps(acertado)
                                            UDPServerSocket.sendto(str.encode(acertado1, address1))
                                            game_board2[row2][col2] = Fore.RED + "X" + Style.RESET_ALL
                                        else:
                                            print("¡Jugador 2 ha fallado!")
                                            game_board2[row2][col2] = Fore.GREEN + "X" + Style.RESET_ALL
                                            errado1 = json.dumps(errado)
                                            UDPServerSocket.sendto(str.encode(errado1, address1))
                                        shots2.append((row2, col2))

                                        if check_victory(game_board2):
                                            print("Jugador 2 (bot) gana. ¡Felicidades!")
                                            perdio1 = json.dumps(perdio)
                                            UDPServerSocket.sendto(str.encode(perdio1, address1))
                                            break
                                        print_game_boards(game_board1, game_board2, shots1, shots2)
                                except Exception as error:
                                    print("Error: ", error)
                                UDPServerSocket.sendto(str.encode(PedirBarquitos1), address1)
                                
                        else:
                            print("otra cosa recibida")
                            print("json: ")
                            print(json.dumps(received_data2, indent=4))
        else:
            print("Error al recibir el mensaje de coneccion de un usuario.")

    except json.JSONDecodeError:
        print("Error: El mensaje recibido no es un JSON válido.")

# No es necesario cerrar el socket del servidor en este ejemplo
