import speech_recognition as sr
import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


def audioSplitter(newFileName):
    audioFileDir = os.path.join(os.getcwd(), "app", "auds", newFileName)
    # print(audioFileDir);
    sound = AudioSegment.from_file(audioFileDir)
    tempVar = 1  # holds file name which is a number.
    for i in range(0, round(len(sound)/1000), 120):
        if((len(sound)-i*1000) <= 120000):
            # here only when time remaining to process is less than 2 mins.
            break
        sound[i*1000:(i+120)*1000].export(os.path.join(os.getcwd(),
                                                       "app", "chunks", f"{tempVar}.wav"), format="wav")
        # print(f"{i*1000}:{(i+120)*1000}_______{tempVar}.wav");
        tempVar += 1
    sound[(tempVar-1)*120000:len(sound)
          ].export(os.path.join(os.getcwd(), "app", "chunks", f"{tempVar}.wav"), format="wav")
    # print(f"{i*1000}:{(i+120)*1000}_______{tempVar}.wav");


def toWav(fileName):  # has  extension mp4;
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

    newFileName += ".wav"  # gives the name of the wav file.

    video.audio.write_audiofile(os.path.join(
        os.getcwd(), "app", "auds", newFileName), codec='pcm_s16le')  # writes to file

    audioSplitter(newFileName)  # calls to cut the audio files.

    # return
    # returns name with wav extension


# takes mp4 file name and converts it to wav internally.
def textExtractor(fileName):
    # wavFileName = toWav(fileName)  # has extension wav.
    # toWav(fileName)
    chunksPath = os.path.join(os.getcwd(), "app", "auds")
    textValue = ""
    rec = sr.Recognizer()

    for root, dir, files in os.walk(os.path.join(os.getcwd(), "app", "chunks")):
        for name in files:
            if ".wav" in name:

                with sr.AudioFile(os.path.join(os.getcwd(), "app", "chunks", name)) as source:
                    # rec.adjust_for_ambient_noise(source, duration=1)
                    audio = rec.record(source)
                    text = rec.recognize_google(audio)
                    print(os.path.join(os.getcwd(), "app", "chunks", name)+"\n");
                    print(text)
                    textValue += text

    return textValue
