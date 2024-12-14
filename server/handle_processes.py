from config.settings import DISCONNECT_COMMAND, MAX_PROCESS_COUNT
from server.settings import server_running
from classes.server import Server
from classes.connection import Connection
from log import log_server
import multiprocessing
import multiprocessing.synchronize
import threading
import time


process_dict: dict[int, multiprocessing.Process] = {}
process_lock = threading.Lock()


def add_worker(
        process_id: int, 
        lock: multiprocessing.synchronize.Lock, 
        connection: Connection, 
        address: tuple[str, int]
    ):
    process = multiprocessing.Process(target=handle_client, args=(lock, connection, address))
    process.start()
    with process_lock:  # Lock to safely modify the shared dictionary
        process_dict[process_id] = process


def monitor_processes():
    while True:
        with process_lock:
            for name, process in list(process_dict.items()):
                if not process.is_alive():  # Check if the process is still running
                    process.join()          # Ensure resources are cleaned up
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


def handle_client(lock: multiprocessing.synchronize.Lock, connection: Connection, address: tuple[str, int]):
    with connection:
        async_log(lock, f"Connected with {address[0]}:{address[1]}")

        while True:
            received = connection.recv_decoded()

            if received:
                if received == DISCONNECT_COMMAND:
                    break
                
                async_log(lock, received)

            # Exit condition: The server is not running anymore
            with server_running.get_lock():
                if not server_running.value:
                    break
        
        async_log(lock, f"{address[0]}:{address[1]} disconnected")


def async_log(
        lock: multiprocessing.synchronize.Lock, 
        message: str
    ):
    lock.acquire()
    log_server.send(message)
    lock.release()
