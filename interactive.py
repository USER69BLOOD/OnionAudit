from msgs import *
from utils import clear_screen, is_valid_onion
import time
import sys
from tor_search import search, check_onion, live_check

def run():
    onions = set()

    clear_screen()
    show_banner()

    while True:
        print()
        choice = show_menu()

        try:
            choice = int(choice)
        except:
            print(log("Input Should be Number and in Range.", "error"))
            time.sleep(1)
            continue

        if choice > 6 or choice < 1:
            print(log("Choose From the Menu.", "error"))
            time.sleep(1)
            continue
            

        if choice < 5:
            sources = ""
            if choice == 1:
                sources = "AHMIA"
            if choice == 2:
                sources = "TOR66"
            if choice == 3:
                sources = "TORCH"
            if choice == 4:
                sources = None
            

            
            keyword = input(Fore.MAGENTA + "Enter search keyword: " + Fore.WHITE).strip()
            print(log(f"Searching {sources} for '{keyword}'...", "info"))
            onions = search(keyword, sources)

            print(log(f"Found {len(onions)} potential onion addresses.", "success"))

            if len(onions) == 0:
                print(log(f"Might some error.......", "warn"))
                time.sleep(2)
                continue

            # live check
            live_c =  input(f"{Fore.GREEN}Want to check if they are live (Y/n)? {Fore.WHITE}")

            live = False
            if live_c.lower() not in ('y', 'n'):
                print(log("Bad input!", "warn"))
            elif live_c.lower() == 'y':
                live = True


            with open("fetched_onions.txt", "a", encoding="utf-8") as fetched, open("live_onions.txt", "a", encoding="utf-8") as livef:
                for onion in onions:
                    print(log(f"fetched onion : {onion}", "info"))
                    fetched.write(onion + "\n")
                    if live and check_onion(onion):
                        print(log(f"Check if Live : {onion}", "success"))
                        livef.write(onion + "\n")


            print(log(f"fetched Onions saved to fetched_onion.txt file.", "success"))
            if live:
                print(log(f"live Onions saved to live_onions.txt file.", "success"))


        if choice == 5:
            address = input("Enter the onion address : ")

            print(log(f"Checking if address is live", "info"))

            live_check(address, False)


        if choice == 6:
            print(log("Exit the tool.", "info"))
            time.sleep(1)
            sys.exit()