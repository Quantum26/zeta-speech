import sys
sys.path.insert(1, '../')
import speech_recognition as sr
import pyaudio
from chrome.websites import open_site
from chrome.youtube_music import youtube_music as music
from tts.tts_funcs import tts
from other_apps.discord import open_discord

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pa = pyaudio.PyAudio

r = sr.Recognizer()

""" Speech-to-text helper function. 
    Use to change speech-to-text API.
    
    Input: Audio file to translate
    Output: Response packet with status and translation/error fields. 
    """
def translate(audio):
    response = {
        "status": True,
        "msg" : None
    }
    try:
        response["msg"] = r.recognize_google(audio).lower()
    except sr.RequestError:
        response["status"] = False
        response["msg"] = "API unavailable"
    except sr.UnknownValueError:
        response["status"] = False
        response["msg"] = "Speech Unrecognizable"
    return response

def listen(mic):
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("listening")
        audio = r.listen(mic)
    response = translate(audio)
    return response

def looped_listen(mic, repeat=2):
    stream = pa.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=CHUNK,
                input=True)
    frames=[]
    err = None
    keyboard.wait("f", suppress=True)
    print('press f to talk, press esc to stop...')
    def release():
        translate(frames)
    def record():
        data = stream.read(CHUNK)
        frames.append(data)


    keyboard.add_hotkey()

    keyboard.wait('esc')

    stream.stop_stream()
    stream.close()

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

    print(response["msg"])
    phrase_arr = response["msg"].split(" ")

    if "open" in phrase_arr[0]:
        if "discord" in phrase_arr[1]:
            tts("Opening discord! awdoisfjoijjfwlaklk")
            open_discord()
        else:
            open_site(phrase_arr[1:])

    elif "play" in phrase_arr[0]:
        music(phrase_arr[1:])

    elif response["status"]:
        tts(response["msg"])