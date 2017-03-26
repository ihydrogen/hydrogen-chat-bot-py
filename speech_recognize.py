#!/usr/bin/env python3
import speech_recognition as sr
import bash

# obtain path to "english.wav" in the same folder as this script
from os import path

def recognize(input):

    AUDIO_FILE = "russian.wav"
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "french.aiff")
    #AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")


    def convert():
        bash.bash("mpg123 -w %s %s" % (AUDIO_FILE, input))


    # use the audio file as the audio source
    r = sr.Recognizer()
    convert()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source) # read the entire audio file

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        return r.recognize_google(audio, language="ru-RU")
    except:
        return ''