from classes.dataclasses import Address, Client
from config.settings import CONNECTED_COMMAND, DISCONNECT_COMMAND, MAX_PROCESS_COUNT
from server.settings import server_running
from classes.server import Server
from classes.connection import Connection
from log import log_server
import multiprocessing
import multiprocessing.synchronize
import threading
import time


process_dict: dict[int, Client] = {}
process_lock = threading.Lock()


def add_worker(
        process_id: int, 
        lock: multiprocessing.synchronize.Lock, 
        connection: Connection, 
        address: Address
    ):
    process = multiprocessing.Process(target=handle_client, args=(lock, connection, address))
    process.start()
    with process_lock:  # Lock to safely modify the shared dictionary
        process_dict[process_id] = Client(connection, process)


def monitor_processes():
    while True:
        with process_lock:
            for name, client in list(process_dict.items()):
                if not client.process.is_alive():  # Check if the process is still running
                    client.process.join()          # Ensure resources are cleaned up
                    del process_dict[name]  # Remove finished process from the dictionary
        time.sleep(0.5)

        # Exit condition: The server is not running anymore
        with server_running.get_lock():
            if not server_running.value:
                break


def handle_processes(server: Server, lock: multiprocessing.synchronize.Lock):
    monitoring_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitoring_thread.start()

    last_id = 0

    while True:
        # This try-except is needed to the server.accept end (timeout exception)
        try:
            conn, addr = server.accept()

            while len(process_dict) >= MAX_PROCESS_COUNT:
                time.sleep(1)
            
            add_worker(last_id, lock, conn, addr)
            last_id += 1
        except:
            pass  # TODO: Improve
        
        # Exit condition: The server is not running anymore
        with server_running.get_lock():
            if not server_running.value:
                break
    
    monitoring_thread.join()


def handle_client(lock: multiprocessing.synchronize.Lock, connection: Connection, address: Address):
    with connection:
        async_log(lock, f"Connected with {address.host}:{address.port}")

        nickname = connection.recv_decoded()

        if not nickname:
            async_log(lock, f"{address.host}:{address.port} did not send a nickname")
            connection.send_decoded("Error: A nickname is required to connect")
            return
        else:
            connection.send_decoded(CONNECTED_COMMAND)

        while True:
            message = connection.recv_decoded()

            if message:
                if message == DISCONNECT_COMMAND:
                    break
                
                broadcast(connection, f"{nickname}: {message}")
                async_log(lock, f"{nickname}: {message}")

            # Exit condition: The server is not running anymore
            with server_running.get_lock():
                if not server_running.value:
                    break
        
        async_log(lock, f"{address.host}:{address.port} disconnected")


def broadcast(sender: Connection, message: str):
    with process_lock:
        for _, client in list(process_dict.items()):
            client.connection.send_decoded(message)


def async_log(
        lock: multiprocessing.synchronize.Lock, 
        message: str
    ):
    lock.acquire()
    log_server.send(message)
    lock.release()
