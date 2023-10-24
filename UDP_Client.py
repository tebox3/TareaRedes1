import socket
import json
from colorama import Fore, Style
import random
import sys

serverAddressPort = ("127.0.0.1", 20001)
bufferSize = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
message = {
    "action": "c",  # Puedes cambiar esta acción según lo que necesites
    "bot": 1,
    "ships": {
        "p": [],
        "b": [],
        "s": []
    },
    "position": []
}
verdad = False
board = []
""" 
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
 """
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

def build_game_board(board):
    for _ in range(5):
        board.append(["O"] * 5)

def place_ships(board,bot):
    place_ship(board, 3, Fore.BLUE + "Y" + Style.RESET_ALL,bot["p"]) #3 casillas
    place_ship(board, 2, Fore.BLUE + "Y" + Style.RESET_ALL,bot["b"]) #2 casillas
    place_ship(board, 1, Fore.BLUE + "Y" + Style.RESET_ALL,bot["s"]) #1 casillas


def place_ship(board, size, symbol,bot):
    while True:
        """ row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        orientation = random.choice(["horizontal", "vertical"]) """

        row = bot[1]
        col = bot[0]

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
verdade = True
while True:
    while True:
        try:
            accion = input("Desea conectarse(si o no): ")
            
            if accion.lower() == 'si':
                message["action"] = "c"

            # Serializar el diccionario JSON a una cadena JSON
            json_message = json.dumps(message)

            # Codificar la cadena JSON como bytes
            bytesToSend = json_message.encode()

            UDPClientSocket.sendto(bytesToSend, serverAddressPort)

            msgFromServer, serverAddress = UDPClientSocket.recvfrom(bufferSize)

            break
        except:
            print("No se puedo conectar con el servidor")

    try:
        # Deserializar el mensaje JSON recibido
        received_data = json.loads(msgFromServer.decode())
        if received_data["action"]=="c":
            if received_data["status"]==1:
                print("La conexion con el servidor se realizo con exito!")
                verdad = True
        # Imprimir el JSON recibido
        print("Mensaje del servidor:")
        print(json.dumps(received_data, indent=4))
        seleccion = int(input("Desea partida con BOT(1) o jugador (0): "))
        if seleccion == 1:
            print("Eligio partida con BOT")
        if seleccion == 0:
            print("Eligio partida con otro jugador 1v1, esperando conexion del otro jugador...")
        mes1 = {
                        "action": "s",
                        "bot": seleccion,
                        "position": []  # Establece las coordenadas jugadas por el usuario
                        }
        json_message1 = json.dumps(mes1)

        # Codificar la cadena JSON como bytes
        bytesToSend1 = json_message1.encode()
        print("Enviando seleccion")
        UDPClientSocket.sendto(bytesToSend1, serverAddressPort)
        print("enviada seleccion")
        #Enviada solicitud de partida con BOT o Player


        msgFromServer1, serverAddress = UDPClientSocket.recvfrom(bufferSize)
        print("Segundo mensaje del servidor: (deberia contener s en action)")
        received_data2 = json.loads(msgFromServer1.decode())
        print(json.dumps(received_data2, indent=4))
        if received_data2["action"]=="s":
            if received_data2["status"]==1:
                print("Lista la partida.")
            else:
                print("Error1!!!")
        else:
                print("Error2!!!")
        msgFromServer2, serverAddress = UDPClientSocket.recvfrom(bufferSize)
        print("Tercer mensaje del servidor: (deberia contener b en action)")
        received_data3 = json.loads(msgFromServer2.decode())
        print(json.dumps(received_data3, indent=4))
        if received_data3["action"]=="b":
            if received_data3["status"]==1:
                print("Respuesta solicitando barcos")
            else:
                print("Error1!!!")
        else:
                print("Error2!!!")
        x1 = 1
        y1 = 1 
        x2 = 3
        y2 = 2
        x3 = 4
        y3 = 4  
        MandarBarquitos = {
                        "action": "b",
                        "bot": "",
                        "ships": {
                            "p": [x1,y1,1],
                            "b": [x2,y2,0],
                            "s": [x3,y3,0]
                        }  # Establece las coordenadas jugadas por el usuario
                        }
        json_message2 = json.dumps(MandarBarquitos)

        # Codificar la cadena JSON como bytes
        bytesToSend2 = json_message2.encode()
        UDPClientSocket.sendto(bytesToSend2, serverAddressPort)
        msgFromServer3, serverAddress = UDPClientSocket.recvfrom(bufferSize)
        print("CUARTO mensaje del servidor: (deberia contener b en action)")
        received_data4 = json.loads(msgFromServer3.decode())
        print(json.dumps(received_data4, indent=4))
        shots1 = []  # Lista de disparos del Jugador 1
        shots2 = []  # Lista de disparos del Jugador 2
        if received_data4["action"]=="b":
            if received_data4["status"]==1:
                print("Barcos aceptados")
                game_board1 = []
                game_board2 = []
                build_game_board(game_board1)
                build_game_board(game_board2)
                place_ship(game_board1, 3, Fore.BLUE + "Y" + Style.RESET_ALL,MandarBarquitos["ships"]["p"])
                place_ship(game_board1, 2, Fore.BLUE + "Y" + Style.RESET_ALL,MandarBarquitos["ships"]["b"])
                place_ship(game_board1, 1, Fore.BLUE + "Y" + Style.RESET_ALL,MandarBarquitos["ships"]["s"])
                for row in game_board1:
                    print(" ".join(row))
                    while True:
                        print_game_boards(game_board1, game_board2, shots1, shots2)
                        turnomsg, serverAddress = UDPClientSocket.recvfrom(bufferSize)
                        turno1 = json.loads(turnomsg.decode())
                        if turno1["action"] == "l":
                            print("Perdio el juego!")
                            sys.exit()
                            break
                        if turno1["action"] == "w":
                            print("gano el juego!")
                            sys.exit()
                            break
                        if turno1["action"] == "t" and turno1["status"] == 1:
                            try:
                                row1 = int(input("Jugador 1: Ingresa la fila para tu ataque (0-19): "))
                                col1 = int(input("Jugador 1: Ingresa la columna para tu ataque (0-19): "))
                                ataqueJson = {
                                    "action": "a",
                                    "bot": "",
                                    "ships": "",
                                    "position": [row1,col1]
                                }
                                ata2 = json.dumps(ataqueJson)
                                atacc2 = ata2.encode()
                                UDPClientSocket.sendto(str.encode(ata2), serverAddressPort)
                                turnomsg1, serverAddress = UDPClientSocket.recvfrom(bufferSize)
                                jsonataque = json.loads(turnomsg1.decode())
                                if jsonataque["action"] == "a" and jsonataque["status"] == 1 and jsonataque["position"] == [row1,col1]:
                                    print("¡Jugador 1 ha golpeado un barco!")
                                    print(jsonataque)
                                    game_board1[row1][col1] = Fore.RED + "X" + Style.RESET_ALL
                                elif jsonataque["action"] == "a" and jsonataque["status"] == 0 and jsonataque["position"] == [row1,col1]:
                                    print("¡Jugador 1 ha fallado!")
                                    print(jsonataque)
                                    game_board1[row1][col1] = Fore.GREEN + "X" + Style.RESET_ALL
                                else:
                                    print("Respuesta extranaña",jsonataque)
                                shots1.append((row1, col1))
                            except ValueError:
                                print("Entrada no válida. Ingresa un número entre 0 y 19.")


                        elif turno1["action"] == "t" and turno1["status"] == 0:
                            print_game_boards(game_board1, game_board2, shots1, shots2)
                            ataqueBot, serverAddress = UDPClientSocket.recvfrom(bufferSize)
                            jsonataqueJson = json.loads(ataqueBot.decode())
                            if turno1["action"] == "t" and turno1["status"] == 0 and seleccion == 0:
                                print("Esperando ataque del oponente...")
                            if jsonataqueJson["action"] == "a":
                                row2 = jsonataqueJson["position"][0]
                                col2 = jsonataqueJson["position"][1]
                            else:
                                print("mensaje raro 2")
                            if game_board2[row2][col2] == "Y":
                                print("¡Jugador 2 ha golpeado un barco!")
                                game_board2[row2][col2] = Fore.RED + "X" + Style.RESET_ALL
                            else:
                                print("¡Jugador 2 ha fallado!")
                                game_board2[row2][col2] = Fore.GREEN + "X" + Style.RESET_ALL

                            shots2.append((row2, col2))
                            print_game_boards(game_board1, game_board2, shots1, shots2)
                        else:
                            print("Otro mensaje recibido: ",turno1)
    except json.JSONDecodeError:
        print("Error: El mensaje recibido no es un JSON válido.")
    finally:
        jsonDisconnect = {
                        "action": "d",
                        "bot": "",
                        "ships": "",  # Establece las coordenadas jugadas por el usuario
                        "position": ""
                        }
        dissconnected = json.dumps(jsonDisconnect)

        # Codificar la cadena JSON como bytes
        dsc = dissconnected.encode()
        UDPClientSocket.sendto(dsc, serverAddressPort)
        #if (buildear == "si"):
# Cerrar el socket del cliente cuando hayas terminado de usarlo
UDPClientSocket.close()
