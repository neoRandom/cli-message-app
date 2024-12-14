from config.settings import LOG_ADDRESS, LOG_STOP_COMMAND
from classes.connection import Connection
from classes.server import Server
import socket


def handle_connection(connection: Connection):
    with connection:
        while True:
            log = connection.recv_decoded()

            if not log:
                continue

            if log.strip() == LOG_STOP_COMMAND:
                print("Stopping the server...")
                break

            print(log)


def run():
    with Server(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(5)
        server.bind(LOG_ADDRESS)

        server.listen()

        conn, _ = server.accept()
        handle_connection(conn)


if __name__ == "__main__":
    run()
