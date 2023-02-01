import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import requests
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import youtube_dl 
import os 

root = tk.Tk()
root.withdraw()

# Pedir para o usuário inserir o link do vídeo
link = input("Insira o link do vídeo: ")
if "facebook.com" in link:
    path = filedialog.askdirectory()
    os.chdir(path) 
    y = {} 

    # Começar o download 
    with youtube_dl.YoutubeDL(y) as u: 
        u.download([link]) 
    print("Download concluído!") 
else:
    yt = YouTube(link)
print("Escolha o formato de download:")
print("1 - Vídeo")
print("2 - Áudio")

choice = int(input())

if choice == 1:
    print("Resoluções de vídeo disponíveis:")
    formats = yt.streams.filter(file_extension='mp4')
    formats = [f for f in formats if f.resolution is not None]
    formats = sorted(formats, key=lambda x: x.resolution, reverse=True)
    for i, f in enumerate(formats[:3]):
        print(str(i+1) + ": " + f.mime_type + " - " + str(f.resolution))
    choice = int(input("Escolha a resolução desejada: "))
    video = formats[choice - 1]
else:
    print("Formato de áudio disponíveis:")
    formats = yt.streams.filter(only_audio=True)
    for i, f in enumerate(formats):
        print(str(i+1) + ": " + f.mime_type + " - " + str(f.abr))
    choice = int(input("Escolha o formato de áudio desejado: "))
    video = formats[choice - 1]
path = filedialog.askdirectory()

# Começar o download
response = requests.get(video.url, stream=True)
total_size = int(response.headers.get("content-length", 0))
filename = video.default_filename

with open(path+"/"+filename, "wb") as f:
    for data in tqdm(response.iter_content(1024), total=total_size, unit="B", unit_scale=True, desc=filename):
        f.write(data)
print("Download concluído!")
