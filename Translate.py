from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
import time
from threading import Event
from playsound import playsound
import Weather as w
import datetime

r = sr.Recognizer()
mic = sr.Microphone()

global speech_input

def read(text):
    mp3 = BytesIO()
    tts = gTTS(text, 'en')
    tts.save('temp.mp3')
    playsound('temp.mp3')

def callback(recognizer, audio):                          # this is called from the background thread
        try:
            print("You said " + recognizer.recognize_google(audio))  # received audio data, now need to recognize it
        except (sr.UnknownValueError, LookupError):
            print("Oops! Didn't catch that")

r = sr.Recognizer()
r.energy_threshold = 2000
r.listen_in_background(sr.Microphone(), callback)
                                
while True: time.sleep(1)
