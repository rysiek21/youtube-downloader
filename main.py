import sys
import os

import donwloader
import search
from colorama import Fore


def load():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "youtube-downloader 1.0 by rysiek21")
        print(Fore.CYAN + "1. Download from youtube using URL")
        print(Fore.CYAN + "2. Download from youtube using Search")
        print(Fore.CYAN + "3. Exit")
        choice = str(input("What do you want to do [1-3]: " + Fore.RESET))

        if choice == "1":
            donwloader.setup_url_download()
            break
        elif choice == "2":
            search.search()
            break
        elif choice == "3":
            sys.exit()


if __name__ == '__main__':
    load()
