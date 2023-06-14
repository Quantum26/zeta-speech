import pyttsx3 as pytts
from threading import Thread

engine = pytts.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def tts_thread(msg):
    print(msg)
    engine.say(msg)

def tts(msg):
    thread = Thread(target = tts_thread, args = (msg,))
    thread.start()