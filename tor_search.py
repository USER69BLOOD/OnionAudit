import requests
import re
import json
import random
from msgs import log
from utils import clean_url
import time
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
with open("user-agent.json", 'r') as file:
    agents = json.load(file)
    HEADERS["User-Agent"] = random.choice(agents)



ONION_REGEX = re.compile(r"(?:https?://)?[a-z2-7]{16}\.onion|(?:https?://)?[a-z2-7]{56}\.onion")


def check_onion(url):
    if not url.startswith("http://"):
        url = "http://" + url
    try:
        r = requests.get(url, headers=HEADERS, proxies=proxies, timeout=15)
        return r.status_code == 200
    except Exception:
        return False

def search(query, sources: str | None = None):
    
    onions = set()

    source_map = {
        "AHMIA": ["http://juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd.onion", "/?q"],
        "TOR66": ["http://tor66sewebgixwhcqfnp5inzp5x5uohhdy3kvtnyfxc2e5mxiuh34iid.onion","?q" ],
        "TORCH": ["http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion", "?query"]
    }
    


    if not sources:
        sources = "AHMIA, TOR66, TORCH"


    for source in [field.strip() for field in sources.split(",")]:

        try:
            url = source_map[source][0]
            if not check_onion(url):
                print(log(f"Skipping source {source}...Not live."))
                time.sleep(2)
                continue
            print(f"{url}/search{source_map[source][1]}={query}")
            r = requests.get(f"{url}/search{source_map[source][1]}={query}", headers=HEADERS, proxies=proxies, timeout=20)
            r.raise_for_status()

            for match in ONION_REGEX.findall(r.text):
                onions.add(clean_url(match))

        except Exception as e:
            print(log(f"Error searching {source}: {e}", "error"))
            time.sleep(2)
    
    
    return set(onions)
    


