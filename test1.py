#Heavily based off of https://realpython.com/python-speech-recognition/
import speech_recognition as sr
import pyaudio
from websites import open_site
from tts_functions import tts
from discord import open_discord

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pa = pyaudio.PyAudio

r = sr.Recognizer()

""" Speech-to-text helper function. 
    Use to change speech-to-text API.
    
    Input: Audio file to translate
    Output: Response packet with success and translation/error fields. 
    """
def translate(audio):
    response = {
        "success": True,
        "message" : None
    }
    try:
        response["message"] = r.recognize_google(audio).lower()
    except sr.RequestError:
        response["success"] = False
        response["message"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["message"] = "Speech Unrecognizable"
    return response

def listen(mic):
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("listening")
        audio = r.listen(mic)
    response = translate(audio)
    return response

def looped_listen(mic, repeat=2):
    audio = None

    response = translate(audio)
    return response

if __name__ == "__main__":
    print("Starting...")
    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if "USB PnP" in mic_name:
            device_index=mic_index
            print("mic chosen: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)
    response = listen(main_mic)
    print(response["message"])

    if "open" in response["message"].split(" ")[0]:
        phrase_arr = response["message"].split(" ")[1:]
        if "discord" in phrase_arr[0]:
            open_discord()
        else:
            open_site(phrase_arr)