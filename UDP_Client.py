import socket
import json
from colorama import Fore, Style
import random


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

    except json.JSONDecodeError:
        print("Error: El mensaje recibido no es un JSON válido.")
    if(verdad):
        buildear = input("Desea enviar posicion barcos al azar(si/no)?: ")
        #if (buildear == "si"):
# Cerrar el socket del cliente cuando hayas terminado de usarlo
UDPClientSocket.close()
