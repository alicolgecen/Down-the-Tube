from pytube import YouTube
from pytube import Playlist
from pydub import AudioSegment
import os

global path
path =  "/Volumes/Volume Name/YouTube/"

def CheckFolder(folder_name):
    os.chdir(path)
    cwd = os.getcwd()
    dir = os.path.join(cwd, folder_name)
    if not os.path.exists(dir):
        os.mkdir(dir)
        print(f"Folder: {folder_name} is created.")

def ReplaceChars(text):
    replace_list = [".", ",", "#", "\'", "\"", "?", "/", "$", "|", "\\", "!", "*"]

    for item in replace_list:
        text = text.replace(item, "")
    return text

def DownloadSingleVideo(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(output_path=path)
    except:
        print(f"There was a problem with {youtubeObject.url}.")

def DownloadPlaylistVideo(link):
    youtubePlaylist = Playlist(link)
    for url in youtubePlaylist.video_urls:
        try:
            video = YouTube(url)
            CheckFolder(youtubePlaylist.title)
            print(f"Downloading: {video.title}")
            video = video.streams.get_highest_resolution()
            video.download(output_path = path + youtubePlaylist.title + "/")
            print(f"Downloaded: {video.title}")
        except:
           print(f"There was a problem with {url}.")

def DownloadSingleAudio(link):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.filter(only_audio = True).first()
    try:
        print(f"Downloading: {youtubeObject.title}")
        youtubeObject.download(output_path=path)
        print(f"Conversion to mp3: {youtubeObject.title}")
        mp4_file = AudioSegment.from_file(path + ReplaceChars(youtubeObject.title) + ".mp4", format="mp4")
        mp4_file.export(path + ReplaceChars(youtubeObject.title) + ".mp3", format="mp3")
        print(f"File is ready: {youtubeObject.title}")
        os.remove(path + ReplaceChars(youtubeObject.title) + ".mp4")
    except:
        print(f"There was a problem with {youtubeObject.title}: {youtubeObject.url}.")

def DownloadPlaylistAudio(link):
    youtubePlaylist = Playlist(link)
    for url in youtubePlaylist.video_urls:
        try:
            video = YouTube(url)
            audio = video.streams.filter(only_audio=True).first()
            CheckFolder(youtubePlaylist.title)
            print(f"Downloading: {video.title}")
            audio.download(output_path=path + youtubePlaylist.title + "/")
            print(f"Conversion to mp3: {video.title}")
            mp4_file = AudioSegment.from_file(path + youtubePlaylist.title + "/" + ReplaceChars(video.title) + ".mp4", format="mp4")
            mp4_file.export(path + youtubePlaylist.title + "/" + ReplaceChars(video.title) + ".mp3", format="mp3")
            print(f"File is ready: {video.title}")
            os.remove(path + youtubePlaylist.title + "/" + ReplaceChars(video.title) + ".mp4")
        except:
            print(f"There was a problem with {video.title}: {url}.")

single_or_playlist = input("Single video/audio or playlist to be downloaded? s for singles, p for playlists: ")
link = input("Enter the URL: ")
purpose = input("Choose what you want to do. v for video a for audio: ")

if str(single_or_playlist).lower() == "s":
    if str(purpose).lower() == "v":
        DownloadSingleVideo(link)
    elif str(purpose).lower() == "a":
        DownloadSingleAudio(link)
    else: print("Wrong input. Start again.")

elif str(single_or_playlist).lower() == "p":
    if str(purpose).lower() == "v":
        DownloadPlaylistVideo(link)
    elif str(purpose).lower() == "a":
        DownloadPlaylistAudio(link)
    else: print("Wrong input. Start again.")

else: print("Wrong input. Start again.")