from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

# Mapping of log levels to tag and color
LOG_LEVELS = {
    "success": (Fore.GREEN + "[+]", Style.BRIGHT),
    "info":    (Fore.CYAN + "[*]", Style.BRIGHT),
    "warn":    (Fore.YELLOW + "[!]", Style.BRIGHT),
    "error":   (Fore.RED + "[-]", Style.BRIGHT),
    "debug":   (Fore.BLUE + "[D]", Style.BRIGHT),
    "critical":(Fore.MAGENTA + "[!]", Style.BRIGHT)
}

def log(message: str, level: str = "info") -> str:
    """
    Returns a timestamped, colored log string.

    Parameters:
        message (str): The message to log.
        level (str): The log level (success, info, warn, error, debug, critical).

    Returns:
        str: Formatted log string (with colors).
    """
    level = level.lower()
    tag, style = LOG_LEVELS.get(level, (Fore.WHITE + "[?]", Style.BRIGHT))
    time_tag = datetime.now().strftime("%H:%M:%S")
    return f"{Fore.MAGENTA}[{time_tag}]{Style.RESET_ALL} {style}{tag}{Style.RESET_ALL} {message}"

def show_banner():
    banner = f""" {Fore.CYAN}
       ___              _                        _                     __   _   _    
     .'   `.           (_)                      / \                   |  ] (_) / |_  
    /  .-.  \ _ .--.   __   .--.   _ .--.      / _ \    __   _    .--.| |  __ `| |-' 
    | |   | |[ `.-. | [  |/ .'`\ \[ `.-. |    / ___ \  [  | | | / /'`\' | [  | | |   
    \  `-'  / | | | |  | || \__. | | | | |  _/ /   \ \_ | \_/ |,| \__/  |  | | | |,  
     `.___.' [___||__][___]'.__.' [___||__]|____| |____|'.__.'_/ '.__.;__][___]\__/  
                        Auditing .onion URLs on the Tor network

    {Style.BRIGHT}By: USER69BLOOD
    Repo: https://github.com/USER69BLOOD/OnionAudit
    
    Disclaimer:
      - This tool is provided strictly for educational and research purposes.
      - Do NOT use this tool to access illegal content. You are solely responsible for your actions.
    """
    print(banner)

def show_menu():
    print(log("===================================", "info"))
    print(log("[1] Ahmia", "info"))
    print(log("[2] TOR66", "info"))
    print(log("[3] Torch", "info"))
    print(log("[4] Ahmia + TOR66 + Torch", "info"))
    print(log("[5] Check Onion", "info"))
    print(log("[6] Exit", "info"))
    print(log("===================================", "info"))
    choice = input(Fore.GREEN + "Select search engine (1-6): " + Fore.WHITE).strip()
    return choice
