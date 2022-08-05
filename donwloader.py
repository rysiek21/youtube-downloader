import os
import progressbar

from pytube import YouTube
from colorama import Fore
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

import main

downloadFilesize = 0
bar = progressbar.ProgressBar(max_value=100)


def setup_url_download():
    os.system('cls' if os.name == 'nt' else 'clear')
    url = input(Fore.CYAN + "YouTube url: " + Fore.RESET)
    yt = YouTube(url, on_progress_callback=progress)
    print(Fore.CYAN + "Loaded " + Fore.RED + yt.title + Fore.CYAN + " Made by " + Fore.RED + yt.author)
    right_video = input(Fore.CYAN + "Do you want to continue" + Fore.RED + " [Y (default)/N]: " + Fore.RESET).upper()
    if right_video == "Y" or right_video == "YES" or right_video == "":
        while True:
            file_format = input(Fore.CYAN + "Which format of file do you want to use " + Fore.RED + " [video (default)/audio]: " + Fore.RESET).upper()
            if file_format == "AUDIO" or file_format == "A":
                download_audio(yt)
                break
            elif file_format == "VIDEO" or file_format == "V" or file_format == "":
                download_video(yt)
                break


def download_audio(yt):
    print(Fore.CYAN + "Available ABR(Average Bitrate): " + Fore.RED, end=" ")
    available_abr = []
    for x in yt.streams.order_by("abr").filter(only_audio=True):
        available_abr.append(x.abr)
    available_abr = list(dict.fromkeys(available_abr))
    for x in available_abr:
        print(x, end=" ")
    chosen_abr = input(Fore.CYAN + "\nChoose abr: " + Fore.RESET)
    if chosen_abr in available_abr:
        stream = yt.streams.filter(only_audio=True, abr=chosen_abr).first()
        global downloadFilesize
        downloadFilesize = stream.filesize
        print(Fore.CYAN + "Approximate file size: " + Fore.RED + str(round(stream.filesize / 1048576, 1)) + "MB")
        save_destination = input(Fore.CYAN + "Save destination: " + Fore.RESET)
        if os.path.exists(save_destination):
            print(Fore.LIGHTYELLOW_EX)
            global bar
            widgets = [
                ' [', progressbar.Timer(), '] ',
                progressbar.Bar(),
                ' (', progressbar.ETA(), ') ',
            ]
            bar.start()
            output_file = stream.download(output_path=save_destination)
            base, ext = os.path.splitext(output_file)
            new_file = base + '.mp3'
            os.rename(output_file, new_file)
            download_complete()
        else:
            i = input(Fore.RED + "[ERROR] Wrong abr! Press 'Enter' to continue...")
            download_audio(yt)
    else:
        i = input(Fore.RED + "[ERROR] Wrong abr! Press 'Enter' to continue...")
        download_audio(yt)


def download_video(yt):
    global bar
    global downloadFilesize
    print(Fore.CYAN + "Available resolutions: " + Fore.RED, end=" ")
    available_resolutions = []
    for x in yt.streams.order_by('resolution').filter():
        available_resolutions.append(x.resolution)
    available_resolutions = list(dict.fromkeys(available_resolutions))
    for x in available_resolutions:
        print(x, end=" ")
    chosen_resolution = input(Fore.CYAN + "\nChoose resolution: " + Fore.RESET)
    if chosen_resolution in available_resolutions:
        print(Fore.CYAN + "Available formats: " + Fore.RED, end=" ")
        available_formats = []
        for x in yt.streams.filter(res=chosen_resolution):
            available_formats.append(x.subtype)
        available_formats = list(dict.fromkeys(available_formats))
        for x in available_formats:
            print(x, end=" ")
        chosen_format = input(Fore.CYAN + "\nChoose extension: " + Fore.RESET)
        if chosen_format in available_formats:
            print(Fore.CYAN + "Available FPS: " + Fore.RED, end=" ")
            available_fps = []
            for x in yt.streams.filter(res=chosen_resolution, subtype=chosen_format):
                available_fps.append(x.fps)
            available_fps = list(dict.fromkeys(available_fps))
            for x in available_fps:
                print(x, end=" ")
            chosen_fps = int(input(Fore.CYAN + "\nChoose fps: " + Fore.RESET))
            if chosen_fps in available_fps:
                stream = yt.streams.filter(subtype=chosen_format, res=chosen_resolution, fps=chosen_fps).first()
                if stream.audio_codec is not None:
                    downloadFilesize = stream.filesize
                    print(Fore.CYAN + "Approximate file size: " + Fore.RED + str(round(stream.filesize / 1048576, 1)) + "MB")
                    save_destination = input(Fore.CYAN + "Save destination: " + Fore.RESET)
                    if os.path.exists(save_destination):
                        print(Fore.LIGHTYELLOW_EX)
                        widgets = [
                            ' [', progressbar.Timer(), '] ',
                            progressbar.Bar(),
                            ' (', progressbar.ETA(), ') ',
                        ]
                        bar.start()
                        output_file = stream.download(output_path=save_destination)
                        download_complete()
                    else:
                        i = input(Fore.RED + "[ERROR] Wrong abr! Press 'Enter' to continue...")
                        main.load()
                else:
                    want_audio = input(Fore.CYAN + "Chosen video resolution haven't own audio. Do you want to download audio too and add it to video?" + Fore.RED + " [Yes (default)/No]: " + Fore.RESET).upper()
                    if want_audio == "Y" or want_audio == "YES" or want_audio == "":
                        audio_stream = yt.streams.filter(only_audio=True).first()
                        downloadFilesize = stream.filesize
                        print(Fore.CYAN + "Approximate file size: " + Fore.RED + str(
                            round((stream.filesize + audio_stream.filesize) / 1048576, 1)) + "MB")
                        save_destination = input(Fore.CYAN + "Save destination: " + Fore.RESET)
                        if os.path.exists(save_destination):
                            print(Fore.LIGHTYELLOW_EX)
                            widgets = [
                                ' [', progressbar.Timer(), '] ',
                                progressbar.Bar(),
                                ' (', progressbar.ETA(), ') ',
                            ]
                            bar.start()
                            output_video_file = stream.download(output_path=save_destination, filename="video." + chosen_format)
                            bar.finish()
                            bar.start()
                            output_audio_file = audio_stream.download(output_path=save_destination, filename="audio.mp3")
                            video = VideoFileClip(output_video_file)
                            audio = AudioFileClip(output_audio_file)
                            audio = audio.subclip(0, video.end)
                            final = video.set_audio(audio)
                            final.write_videofile(stream.title + "." + chosen_format, bitrate="12000k", fps=chosen_fps)
                            os.remove(output_video_file)
                            os.remove(output_audio_file)
                            download_complete()

                        else:
                            i = input(Fore.RED + "[ERROR] Wrong abr! Press 'Enter' to continue...")
                            download_video(yt)
                    elif want_audio == "NO" or want_audio == "N":
                        downloadFilesize = stream.filesize
                        print(Fore.CYAN + "Approximate file size: " + Fore.RED + str(
                            round(stream.filesize / 1048576, 1)) + "MB")
                        save_destination = input(Fore.CYAN + "Save destination: " + Fore.RESET)
                        if os.path.exists(save_destination):
                            print(Fore.LIGHTYELLOW_EX)
                            widgets = [
                                ' [', progressbar.Timer(), '] ',
                                progressbar.Bar(),
                                ' (', progressbar.ETA(), ') ',
                            ]
                            bar.start()
                            output_file = stream.download(output_path=save_destination)
                            download_complete()
                        else:
                            i = input(Fore.RED + "[ERROR] Wrong abr! Press 'Enter' to continue...")
                            download_video(yt)
                    else:
                        i = input(Fore.RED + "[ERROR] Wrong answer! Press 'Enter' to continue...")
                        download_video(yt)
            else:
                i = input(Fore.RED + "[ERROR] Wrong fps! Press 'Enter' to continue...")
                download_video(yt)
        else:
            i = input(Fore.RED + "[ERROR] Wrong extension! Press 'Enter' to continue...")
            download_video(yt)
    else:
        i = input(Fore.RED + "[ERROR] Wrong resolution! Press 'Enter' to continue...")
        download_video(yt)


def progress(chunk: bytes, file_handler, bytes_remaining):
    download_progress = ((downloadFilesize - bytes_remaining) * 100) / downloadFilesize
    bar.update(round(download_progress, 2))


def download_complete():
    bar.finish()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "\n\nDownload Complate")
    to_contiune = input(Fore.CYAN + "Do you want to download another video?" + Fore.RED + " [Y (default)/N]: " + Fore.RESET).upper()
    if to_contiune == "Y" or to_contiune == "YES" or to_contiune == "":
        main.load()
