from config.settings import HOST_ADDRESS
from classes.server import Server
from log import log_server
from server.handle_processes import handle_processes
from server.handle_input import handle_host_input
import socket
import multiprocessing
import multiprocessing.synchronize


def run():
    # Start the server
    with Server(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.settimeout(5)  # Timeout to the server.accept
        server.bind(HOST_ADDRESS)

        print(f"Listening to {HOST_ADDRESS[0]}:{HOST_ADDRESS[1]}")
        server.listen()

        # Get the process locker
        lock = multiprocessing.Lock()

        log_server.start()  # Starting the Log Server (terminal)
        
        # Start the processes
        # It needs both to the input not block the server-related processes and vice-versa
        handle_processes_process = multiprocessing.Process(target=handle_processes, args=(server, lock))
        handle_host_input_process = multiprocessing.Process(target=handle_host_input, args=(server,))

        handle_processes_process.start()
        handle_host_input_process.start()

        handle_processes_process.join()
        handle_host_input_process.join()

        log_server.stop()  # Stopping/closing the Log Server
