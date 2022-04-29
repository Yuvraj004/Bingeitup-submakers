import speech_recognition as sr
import os
from moviepy.editor import VideoFileClip


def toWav(fileName):
    # video = VideoFileClip("vids"+"/"+fileName);
    video = VideoFileClip(os.path.join(os.getcwd(), "app", "vids", fileName))
    dotWhere = 0
    for i in range(-1, -len(fileName), -1):
        if (fileName[i] == "."):
            dotWhere = len(fileName) + i
            # all this shit just to change extension to wav.GOD help.
            break
    newFileName = ""
    for i in range(0, dotWhere):
        newFileName += fileName[i]

    newFileName += ".wav"
    video.audio.write_audiofile(os.path.join(os.getcwd(), "app", "auds",
                                             newFileName),
                                codec='pcm_s16le')
    print(newFileName)
    return newFileName
    #returns name with wav extension


def textExtractor(
        fileName):  #takes mp4 file name and converts it to wav internally.
    wavFileName = toWav(fileName)  #has extension wav.

    rec = sr.Recognizer()

    with sr.AudioFile(os.path.join(os.getcwd(), "app", "auds",
                                   wavFileName)) as source:
        rec.adjust_for_ambient_noise(source, duration=1)
        audio = rec.record(source)
        textvalue = rec.recognize_google(audio)
    return textvalue
