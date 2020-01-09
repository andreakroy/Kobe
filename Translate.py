from gtts import gTTS
import speech_recognition as sr
from io import BytesIO
import time
from threading import Event
from playsound import playsound

r = sr.Recognizer()
m = sr.Microphone()

global speech_input

def read(text):
    mp3 = BytesIO()
    tts = gTTS(text, 'en')
    tts.save('temp.mp3')
    playsound('temp.mp3')

def callback(recognizer, audio):
    try:
        #read(recognizer.recognize_google(audio))
        speech_input =  recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def listen_for_key():
    with m as source:
        r.energy_threshold = 300
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source)
    while x == True:
        stop = r.listen_in_background(m, callback)
        time.sleep(1)
        if speech_input = 'kobe':
    
listen_for_key()
time.sleep(20)

