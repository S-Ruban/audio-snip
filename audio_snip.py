from pydub import AudioSegment
from tkinter import *
from tkinter import filedialog
import os
import json
import eyed3
import re


def changedir():
    folder.set(filedialog.askdirectory())
    if len(folder.get()) != 0:
        curdir.config(text="Current directory : " + folder.get())
    else:
        curdir.config(text="Current directory : " + os.getcwd())


def down():
    link = url.get()
    os.system("yt-dlp --write-info-json --skip-download " + link)
    os.system("ren *.json metadata.json")
    with open("metadata.json") as json_file:
        md = json.load(json_file)
    os.system(
        'yt-dlp -o "%(title)s.%(ext)s" --extract-audio --audio-format mp3 ' + link
    )
    yt_album = AudioSegment.from_mp3(md["title"] + ".mp3")
    for song in md["chapters"]:
        start_time = int(float(song["start_time"]) * 1000)
        title = song["title"]
        end_time = int(float(song["end_time"]) * 1000)
        title = re.sub("[0-9]*\. ", "", title)
        print(start_time, title, end_time)
        track = yt_album[start_time:end_time]
        track.export(folder.get() + "//" + title + ".mp3", format="mp3")
        audiofile = eyed3.load(folder.get() + "\\" + title + ".mp3")
        audiofile.tag.artist = artist.get()
        audiofile.tag.album = album.get()
        audiofile.tag.save()
    os.system('del "' + md["title"] + '.mp3"')
    os.system("del /f metadata.json")
    url.delete(0, END)
    url.insert(0, "")
    artist.delete(0, END)
    artist.insert(0, "")
    album.delete(0, END)
    album.insert(0, "")


gui = Tk(className="Snip album into individual songs (with metadata)")
gui.geometry("600x200")
folder = StringVar()
Label(gui, text="URL : ").place(x=5, y=10)
url = Entry(gui, width=75)
url.place(x=50, y=10)
Label(gui, text="Artist : ").place(x=5, y=40)
artist = Entry(gui, width=50)
artist.place(x=50, y=40)
Label(gui, text="Album : ").place(x=5, y=70)
album = Entry(gui, width=50)
album.place(x=60, y=70)
curdir = Label(gui, text="Current directory : " + os.getcwd())
curdir.place(x=5, y=130)
chdir = Button(
    gui, text="Change Directory", width=20, height=1, command=changedir
).place(x=425, y=125)
conv = Button(gui, text="Download", width=10, height=1, command=down).place(
    x=250, y=100
)

gui.mainloop()
