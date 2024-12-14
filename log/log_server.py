from config.settings import LOG_ADDRESS, LOG_STOP_COMMAND
from classes.connection import Connection
from time import sleep
import socket
import os


__running = False
__log_connection: Connection | None = None


def start():
    global __running, __log_connection

    if not __running:
        os.system(f"gnome-terminal -- bash -c 'python3 -m log.run_log_server'")
        sleep(1)
        __log_connection = Connection(socket.AF_INET, socket.SOCK_STREAM)
        __log_connection.connect(LOG_ADDRESS)
        __running = True
    else:
        print("Server already running")


def send(message: str = ""):
    global __log_connection
    
    if __log_connection is not None:
        if message == LOG_STOP_COMMAND:
            stop()
        else:
            __log_connection.send_decoded(message)


def stop():
    global __running, __log_connection

    if __log_connection is not None:
        __log_connection.send_decoded(LOG_STOP_COMMAND)
        __log_connection.close()
        __log_connection = None
        __running = False
    else:
        print("Server already stopped")
