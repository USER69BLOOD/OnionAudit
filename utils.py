import os
import re

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


