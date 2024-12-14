from ctypes import c_bool
import multiprocessing

server_running = multiprocessing.Value(c_bool, True)
