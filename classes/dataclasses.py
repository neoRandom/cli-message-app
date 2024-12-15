from classes.connection import Connection
from dataclasses import dataclass
import multiprocessing

@dataclass
class Address:
    host: str
    port: int

@dataclass
class Client:
    connection: Connection
    process: multiprocessing.Process
