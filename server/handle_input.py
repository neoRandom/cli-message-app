from config.settings import HOST_STOP_COMMAND
from server.settings import server_running
from classes.server import Server
import sys


def handle_host_input(server: Server):
    sys.stdin = open(0)  # This is required to prevent the input EOF error

    while True:
        user_input = input("> ")

        # Check if the host admin send a command to stop the server
        if user_input.strip() == HOST_STOP_COMMAND:
            with server_running.get_lock():
                server_running.value = False
            
            server.close()
            break
