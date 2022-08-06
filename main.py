import sys
import os
import donwloader
import search
import updates

from colorama import Fore

version = "1.0.2"


def load():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.RED + "youtube-downloader 1.0.2 by rysiek21")
        print(Fore.CYAN + "1. Download from youtube using URL")
        print(Fore.CYAN + "2. Download from youtube using Search")
        print(Fore.CYAN + "3. Check for updates")
        print(Fore.CYAN + "4. Exit")
        choice = str(input("What do you want to do [1-4]: " + Fore.RESET))

        if choice == "1":
            donwloader.setup_url_download()
            break
        elif choice == "2":
            search.search()
            break
        elif choice == "3":
            updates.check(version)
            break
        elif choice == "4":
            sys.exit()


if __name__ == '__main__':
    load()
