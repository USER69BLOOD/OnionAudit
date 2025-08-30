import os
import re
import tor_search
from msgs import log

def is_valid_onion(url: str) -> bool:
    """
    Check if the URL is a valid .onion link (v2 or v3).
    Returns True if valid, False otherwise.
    """
    url = url.strip()
    onion_regex = r'(?:https?://)?[a-z2-7]{16}\.onion|(?:https?://)?[a-z2-7]{56}\.onion'
    return bool(re.match(onion_regex, url))

def clean_url(url: str) -> str:
    """
    Remove leading/trailing spaces and trailing slashes from a URL.
    """
    return url.strip().rstrip('/')

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def live_check(address, quiet):
    if is_valid_onion(address):
        if tor_search.check_onion(address):
            if not quiet:
                print(log(f"Found live : {address}", "success"))
            return True
        else:
            if not quiet:
                print(log(f"Not live : {address}"), "error")
            return False
    else:
        print(log(f"Error address : {address}", "error"))
        return False

