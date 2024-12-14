from config.settings import LOG_ADDRESS, LOG_STOP_COMMAND
import socket


if __name__ == "__main__":
    from classes.server import Server

    def run():
        with Server(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.settimeout(5)
            server.bind(LOG_ADDRESS)

            server.listen()

            conn, _ = server.accept()
            with conn:
                while True:
                    log = conn.recv_decoded()

                    if not log:
                        continue

                    if log.strip() == LOG_STOP_COMMAND:
                        print("Stopping the server...")
                        break

                    print(log)
    
    run()
