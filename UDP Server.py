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
                    if action1 == "s" and bot1 == "0":
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
                            action2 = received_data2["action"]
                            bot2 = received_data1["bot"]
                            ships = received_data1["ships"]
                            if action2 == "b" and bot2 == "":
                                try:
                                        bot2["p"]
                                        bot2["b"]
                                        bot2["s"]
                                except:
                                    print("El arreglo de barcos entregado por el cliente es incorrecto")
        else:
            print("Error al recibir el mensaje de coneccion de un usuario.")

    except json.JSONDecodeError:
        print("Error: El mensaje recibido no es un JSON válido.")

# No es necesario cerrar el socket del servidor en este ejemplo
