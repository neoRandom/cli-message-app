from classes.connection import Connection
import socket


class Server(socket.socket):
    def __init__(self, *args, **kwargs):   # type: ignore
        super().__init__(*args, **kwargs)  # type: ignore

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

        return (
            new_conn, 
            client_address
        )
