import config.terminal as terminal
import server.host as host
import client.client as client


def select_mode():
    """Prompt the user to select a mode (Host or Client)"""
    mode = input("Select your mode:\n[H]ost\n[C]lient\n: ").strip()

    if not mode:
        print("Error: No mode selected.")
        return None

    return mode[0].lower()


def run():
    mode = select_mode()

    if mode is None:
        return
    
    terminal.clear_screen()

    if mode not in ("h", "c"):
        print("Error: Invalid mode selected. Please choose 'H' for Host or 'C' for Client.")
        return

    match mode:
        case "h":
            print("Host mode selected")
            terminal.clear_screen()
            host.run()
        case "c":
            print("Client mode selected")
            terminal.clear_screen()
            client.run()


if __name__ == "__main__":
    terminal.enter_alt_screen()
    try:
        run()
        print("Press enter to continue", end="")
        terminal.pause()
    except:
        pass
    finally:
        terminal.exit_alt_screen()
