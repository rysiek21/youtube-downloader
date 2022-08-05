import requests
import main

from colorama import Fore


def check(version):
    print(Fore.CYAN + "Current version: " + Fore.RED + version)
    print(Fore.CYAN + "Checking for updates...")
    response = requests.get("https://api.github.com/repos/rysiek21/youtube-downloader/releases/latest")
    if response.status_code == 200:
        data = response.json()
        if data["tag_name"] != version:
            print(Fore.CYAN + "New version available: " + Fore.RED + data["tag_name"])
            print(Fore.CYAN + "Download link: " + Fore.RED + data["assets"][0]["browser_download_url"])
            print(Fore.CYAN + "Changelog: " + Fore.RED + data["body"])
        else:
            print(Fore.CYAN + "No updates available")
    else:
        print(Fore.RED + "[Error] Could not check for updates")
    i = input(Fore.CYAN + "\nPress 'Enter' to continue..." + Fore.RESET)
    main.load()

