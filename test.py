import multiprocessing
import threading
import time

def worker_function(name: str, duration: int):
    """Worker function that simulates work with a sleep."""
    print(f"Process {name} started.")
    time.sleep(duration)
    print(f"Process {name} finished.")

# Dictionary to store processes
process_dict: dict[str, multiprocessing.Process] = {}
process_lock = threading.Lock()  # Lock to synchronize access to the process dictionary

def add_process(name: str, duration: int):
    """Add a new process to the dictionary in a thread-safe way."""
    process = multiprocessing.Process(target=worker_function, args=(name, duration))
    process.start()
    with process_lock:  # Lock to safely modify the shared dictionary
        process_dict[name] = process

def monitor_processes():
    """Monitor and clean up finished processes from the dictionary."""
    while True:
        print(len(process_dict))
        with process_lock:  # Lock to safely iterate over the shared dictionary
            for name, process in list(process_dict.items()):
                if not process.is_alive():  # Check if the process is still running
                    process.join()  # Ensure resources are cleaned up
                    del process_dict[name]  # Remove finished process from the dictionary
                    print(f"Process {name} has been removed.")
        time.sleep(0.5)  # Avoid busy-waiting with a small delay

        # Exit condition (optional): Stop monitoring if no processes exist
        with process_lock:
            if not process_dict:
                break

if __name__ == "__main__":
    # Start the monitoring thread
    monitoring_thread = threading.Thread(target=monitor_processes, daemon=True)
    monitoring_thread.start()

    # Simulate adding processes dynamically
    add_process("Task1", 3)
    time.sleep(1)  # Delay to simulate dynamic addition
    add_process("Task2", 5)
    time.sleep(1)
    add_process("Task3", 2)

    # Wait for all processes to complete (optional)
    monitoring_thread.join()

    print("All processes are finished.")
