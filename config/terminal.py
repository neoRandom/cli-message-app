import sys

# Define color codes
NRM = "\x1B[0m"
RED = "\x1B[1;31m"
GRN = "\x1B[1;32m"
YEL = "\x1B[1;33m"
BLU = "\x1B[1;34m"
MAG = "\x1B[1;35m"
CYN = "\x1B[1;36m"
WHT = "\x1B[1;37m"

B_NRM = "\x1B[0m"
B_RED = "\x1B[0;31m"
B_GRN = "\x1B[0;32m"
B_YEL = "\x1B[0;33m"
B_BLU = "\x1B[0;34m"
B_MAG = "\x1B[0;35m"
B_CYN = "\x1B[0;36m"
B_WHT = "\x1B[0;37m"

BG_NRM = "\x1B[40m"
BG_RED = "\x1B[41m"
BG_GRN = "\x1B[42m"
BG_YEL = "\x1B[43m"
BG_BLU = "\x1B[44m"
BG_MAG = "\x1B[45m"
BG_CYN = "\x1B[46m"
BG_WHT = "\x1B[47m"

def clear_screen():
    sys.stdout.write("\033[H\033[2J\033[3J")

def move_cursor(y: int, x: int):
    sys.stdout.write(f"\033[{y};{x}H")

def enter_alt_screen():
    sys.stdout.write("\033[?1049h\033[H")

def exit_alt_screen():
    sys.stdout.write("\033[?1049l")

def reset_cursor():
    clear_screen()
    move_cursor(1, 0)

def pause():
    sys.stdout.write("\033[8m")  # Hide cursor
    input()  # Wait for user input
    sys.stdout.write("\033[0m")  # Show cursor again

# Example usage
if __name__ == "__main__":
    clear_screen()
    move_cursor(10, 10)
    print(f"{RED}Hello, World!{NRM}")
    pause()
