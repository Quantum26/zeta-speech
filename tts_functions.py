import pyttsx3 as pytts
from threading import Thread

def tts(msg):
    thread = Thread(target = pytts.speak, args = (msg,))
    print(msg)
    thread.start()