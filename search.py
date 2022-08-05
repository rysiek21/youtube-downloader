from pytube import Search
import sys
import donwloader

from colorama import Fore


def search():
    count = 1
    title = input(Fore.CYAN + "Video title: " + Fore.RESET)
    search = Search(title)
    for x in search.results:
        hours = 0
        minutes = 0
        seconds = 0
        remaining = x.length
        while remaining != 0:
            if remaining % 3600 != remaining:
                hours += 1
                remaining -= 3600
            if remaining % 60 != remaining:
                minutes += 1
                remaining -= 60
            else:
                seconds = remaining
                remaining = 0
        print(Fore.RED + str(count) + ". " + Fore.CYAN + x.title + Fore.RED + " length: " + Fore.CYAN + str(hours) + ":" + str(minutes) + ":" + str(seconds) + Fore.RED + " author: " + Fore.CYAN + x.author)
        count += 1
    chosen_video = input(Fore.CYAN + "Number of video to download" + Fore.RED + " ['exit' to leave]: " + Fore.RESET)
    if chosen_video == "exit":
        sys.exit()
    else:
        while True:
            file_format = input(
                Fore.CYAN + "Which format of file do you want to use " + Fore.RED + " [video (default)/audio]: " + Fore.RESET).upper()
            if file_format == "AUDIO" or file_format == "A":
                donwloader.download_audio(search.results[int(chosen_video) - 1])
                break
            elif file_format == "VIDEO" or file_format == "V" or file_format == "":
                donwloader.download_video(search.results[int(chosen_video) - 1])
                break
