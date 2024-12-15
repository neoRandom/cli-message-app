from config import terminal
from config.settings import CONNECTED_COMMAND, DISCONNECT_COMMAND
from classes.connection import Connection
import threading
import socket


connected = False
lock = threading.Lock()


def handle_input(connection: Connection):
    global connected

    while True:
        message = input()
        if message.strip() == "":
            break

        connection.send_decoded(message=message)

        if message.strip() == DISCONNECT_COMMAND:
            print("Disconnected by the client")
            with lock:
                connected = False
            break

        with lock:
            if not connected:
                break


def handle_broadcast(connection: Connection):
    global connected

    while True:
        message = connection.recv_decoded()

        if message:
            if message == DISCONNECT_COMMAND:
                print("Disconnected by the server")
                with lock:
                    connected = False
                break
            else:
                print(message)

        with lock:
            if not connected:
                break


def run():
    global connected

    host_host = input("Host: ")
    host_port = int(input("Port: "))
    nickname  = input("Nickname: ")

    if not host_host or not host_port or not nickname:
        print("Host, port, and nickname are required")
        return
    
    terminal.clear_screen()

    with Connection(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host_host, host_port))
        client.send_decoded(nickname)
        response = client.recv_decoded()

        if response != CONNECTED_COMMAND:
            print(response)
            return
        
        connected = True

        input_thread = threading.Thread(target=handle_input, args=(client,))
        broadcast_thread = threading.Thread(target=handle_broadcast, args=(client,))

        input_thread.start()
        broadcast_thread.start()

        input_thread.join()
        broadcast_thread.join()

        connected = False
