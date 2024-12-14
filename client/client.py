from config.settings import DISCONNECT_COMMAND, HOST_ADDRESS
from classes.connection import Connection
import socket


def run():
    with Connection(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(HOST_ADDRESS)

        while True:
            message = input("> ")
            if message.strip() == "":
                break

            client.send_decoded(message=message)

            if message.strip() == DISCONNECT_COMMAND:
                print("Disconnected by the client")
                break
