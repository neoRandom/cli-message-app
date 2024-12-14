from config.settings import LOG_ADDRESS, LOG_STOP_COMMAND
from classes.connection import Connection
from time import sleep
import socket
import os


class LogServer:
    __running = False
    __log_connection: Connection | None = None

    @staticmethod
    def start():
        if not LogServer.__running:
            os.system(f"gnome-terminal -- bash -c 'python3 -m log.run_log_server'")
            sleep(1)
            LogServer.__log_connection = Connection(socket.AF_INET, socket.SOCK_STREAM)
            LogServer.__log_connection.connect(LOG_ADDRESS)
            LogServer.__running = True
        else:
            print("Server already running")

    @staticmethod
    def send(message: str = ""):
        if LogServer.__log_connection is not None:
            if message == LOG_STOP_COMMAND:
                LogServer.stop()
            else:
                LogServer.__log_connection.send_decoded(message)
    
    @staticmethod
    def stop():
        if LogServer.__log_connection is not None:
            LogServer.__log_connection.send_decoded(LOG_STOP_COMMAND)
            LogServer.__log_connection.close()
            LogServer.__log_connection = None
            LogServer.__running = False
        else:
            print("Server already stopped")
