# CLI Message App

Made with Python 3.13, no use of third-party libraries.

## How to use

### Prerequisites

- A computer
- Python 3.13 (but probably also works on 3.12)
- Linux (but probably also works on MacOS and maybe Windows if you try hard enough)
- GNOME Terminal (this is the reason why you need Linux)

### Running

- In one GNOME Terminal window start the software and select HOST
- In another GNOME Terminal window start the software and select CLIENT
- Send some messages from the client side and see the logs on the host side

### Exiting
- Send `CLOSE_CONNECTION` from the client side to end the connection
- Input `STOP_SERVER` on the HOST panel to properly stop the server
