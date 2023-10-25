import socket
import json
import time
import sys
#25.1.3.172
# Configuración del cliente
serverIP = "25.0.11.160"
serverPort = 20001
bufferSize = 1024

# Crear un socket UDP
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Conectar al servidor
serverAddress = (serverIP, serverPort)

# Solicitar iniciar una partida
msg = {
    "action": "c",
    "bot": 1,
    "ships": {
        "p": [1, 2, 0],
        "b": [3, 4, 1],
        "s": [5, 6, 0]
    },
    "position": [7, 8]
}

barcos = ["p", "b", "s"]
nombreBarcos = ["Patrullero", "Barco", "Submarino"]

UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddress)

def recibir_y_mostrar_mensaje(client_socket):
    msgFromServer, serverAddress = client_socket.recvfrom(bufferSize)
    try:
        decoded_msg = json.loads(msgFromServer.decode())
        if "message" in decoded_msg:
            print(f"Mensaje del servidor: {decoded_msg['message']}")
        # Puedes agregar más lógica para manejar otros tipos de mensajes
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON data from the server")
    except Exception as e:
        print(f"An error occurred: {e}")

def configBarcos(status):
    if (status == 1):
        msg["action"] = "b"
        orientacion = 0
        print("A continuacion ingrese las posiciones de los 3 barcos")
        for i in range(3):
            print("Ingrese el barco n°", i+1, " , tipo: ", nombreBarcos[i], " : ")
            x = input("Ingrese posicion fila: ")
            y = input("Ingrese posicion columna: ")
            if (nombreBarcos[i] != "Barco"):
                orientacion = input("Ingrese la orientacion del barco: 0:Vertical ; 1:Horizontal : ")
            msg["ships"][barcos[i]] = [x, y, orientacion]
            print("--------------------------------------------------------------------------")
    UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddress)

def ataque(status):
    if (status == 1):
        msg["action"] = "a"
        print("A continuacion ingrese una coordenada para realizar un ataque")
        x = input("Ingrese una posicion fila: ")
        y = input("Ingrese una posicion columna: ")
        msg["position"] = [x, y]
    UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddress)

def desconectar(status):
    if (status == 1):
        msg["action"] = "d"
        print("A continuacion se desconectara del servidor")
    UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddress)
    confirmacion = True
    while (confirmacion):
            data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
            mensaje = json.loads(data.decode())
            #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
            if ((mensaje["action"] == "d") and (mensaje["status"] == 1)):
                print("Desconectando del servidor...")
                sys.exit()
            else:
                print("ha ocurrido un problema")
                confirmacion = False

def iniciarJuego():
    print("--------------------------------------------------------------------------")
    print("Conexion establecida con el servidor")
    select = input("Seleccione un modo de juego, 0: vs jugador ; 1: vs bot : ")
    msg["action"] = "s"
    msg["bot"] = select
    UDPClientSocket.sendto(json.dumps(msg).encode(), serverAddress)
    confirmacion = True
    while (confirmacion):
            data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
            mensaje = json.loads(data.decode())
            #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
            if ((mensaje["action"] == "s") and (mensaje["status"] == 1)):
                print("Preparando el inicio del juego...")
                confirmacion = False
            else:
                print("ha ocurrido un problema")
                confirmacion = False




""" def confirmacion(action):
    confir = True
    while (confir):
        data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
        mensaje = json.loads(data.decode())
        print(f"Mensaje del Server ({clientAddress}): {mensaje}")
        if ((mensaje["action"] == action) and (mensaje["status"] == 1)):
            print("Respuesta del servidor exitosa")
            confirmacion = False
        else:
            print("ha ocurrido un problema")
            confirmacion = False """

opciones = {
    "1": configBarcos,
    "2": ataque,
    "3": desconectar
}

while True:
    # Aquí deberías implementar la lógica para que el cliente realice
    # acciones como ataques y envíe los datos al servidor.
    # También deberías recibir las actualizaciones del servidor y
    # mostrarlas al usuario.
    data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
    mensaje = json.loads(data.decode())
    print(f"Mensaje del Server ({clientAddress}): {mensaje}")

    #Conexion con el servidor
    if ((mensaje["action"] == "c") and (mensaje["status"] == 1)):
        iniciarJuego()
    """ if ((mensaje["action"] == "s") and (mensaje["status"] == 1)):
        print("Preparando el inicio del juego") """
    if ((mensaje["action"] == "b") and (mensaje["status"] == 1)):
        print("Es el momento de posicionar los barquitos")
        configBarcos(mensaje["status"])
        confirmacion = True
        while (confirmacion):
            data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
            mensaje = json.loads(data.decode())
            #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
            if ((mensaje["action"] == "b") and (mensaje["status"] == 1)):
                print("Los barquitos se han posicionado sin problemas")
                confirmacion = False
            else:
                print("ha ocurrido un problema, los barquitos no se posicionaron bien")
                confirmacion = False

    elif ((mensaje["action"] == "l") and (mensaje["status"] == 1)):
        print("Hemos perdido!!! :((")
        sys.exit()
    elif ((mensaje["action"] == "w") and (mensaje["status"] == 1)):
        print("HEMOS GANADO EL GAME")
        sys.exit()

    elif (mensaje["action"] == "t"):
        if (mensaje["status"] == 1):
            seguir = input("a: Atacar ; d: Desconectarse => ")
            if (seguir == "a"): 
                print("Es momento del ataque!!")
                ataque(mensaje["status"])
                confirmacion = True
                while (confirmacion):
                    data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
                    mensaje = json.loads(data.decode())
                    #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
                    if ((mensaje["action"] == "a") and (mensaje["status"] == 1)):
                        print("Se hizo el ataque sin problemas")
                        confirmacion = False
                    else:
                        print("tuvimos un error al momento de realizar el ataque")
                        confirmacion = False
            else:
                desconectar(mensaje["status"])

        else:
            print("Es momento de esperar")
            confirmacion = True
            while (confirmacion):
                data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
                mensaje = json.loads(data.decode())
                #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
                if (mensaje["action"] == "a"):
                    if (mensaje["status"] == 1):
                        print("NOS DIERON en la posicion: ", mensaje["position"])
                    else:
                        print("No nos dieron, el rival ataco en: ", mensaje["position"])

                elif ((mensaje["action"] == "w") and (mensaje["status"] == 1)):
                    print("HEMOS GANADO EL GAME")
                    print("Desconectando del servidor...")
                    sys.exit()

                elif ((mensaje["action"] == "l") and (mensaje["status"] == 1)):
                    print("Hemos perdido!!! :((")
                    sys.exit()

                elif ((mensaje["action"] == "t") and (mensaje["status"] == 1)):
                    seguir = input("a: Atacar ; d: Desconectarse => ")
                    if (seguir == "a"): 
                        print("Es momento del ataque!!")
                        ataque(mensaje["status"])
                        confirmacion = True
                        while (confirmacion):
                            data, clientAddress = UDPClientSocket.recvfrom(bufferSize)
                            mensaje = json.loads(data.decode())
                            #print(f"Mensaje del Server ({clientAddress}): {mensaje}")
                            if ((mensaje["action"] == "a") and (mensaje["status"] == 1)):
                                print("Se hizo el ataque sin problemas")
                                confirmacion = False
                            else:
                                print("tuvimos un error al momento de realizar el ataque")
                                confirmacion = False
                    else:
                        desconectar(mensaje["status"])
    print("--------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------")
    #Caso de error
   
"""print("Elige una opción:")
    print("1. Posicionar Barcos")
    print("2. ataque")
    print("3. desconectar")
    opcion = input("Ingrese el número de la opción que desea: ")
    if opcion in opciones:
        opciones[opcion](mensaje["status"]) """
    
