from classes.connection import Connection
from classes.dataclasses import Address
import socket


class Server(socket.socket):
    def __init__(
            self, 
            family: socket.AddressFamily | int = -1,
            type_: socket.SocketKind | int = -1,
            proto: int = -1,
            fileno: int | None = None
        ):   
        super().__init__(family, type_, proto, fileno)

    def accept(self):
        client_socket, client_address = super().accept()

        # Get the File Descriptor of the socket
        fd = socket.dup(client_socket.fileno())

        # Create a Connection (extension of socket.socket)
        new_conn = Connection(
            client_socket.family, 
            client_socket.type, 
            client_socket.proto, 
            fileno=fd
        )

        # Create a Address
        new_addr = Address(
            client_address[0],
            client_address[1]
        )

        return (
            new_conn, 
            new_addr
        )
