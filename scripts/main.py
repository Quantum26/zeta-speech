import sys
sys.path.insert(1, '../')
import speech_recognition as sr
import pyaudio
from assets.tts_funcs import tts
from assets.console import print_sl, clear_terminal_line
from apps.open import open_app
from apps.play import yt_play
import numpy as np
import keyboard
from threading import Thread

commands = {
    "open" : open_app,
    "play" : yt_play
}


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pa = pyaudio.PyAudio()

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

def looped_listen(mic : sr.Microphone, callback = print):
    global running
    global min_noise_level
    running = True
    min_noise_level = 4500

    def escape(_ = None):
        global running
        print("quitting...")
        running = False
    keyboard.add_hotkey('esc', callback=escape, suppress=True)
    print('press f to start, press esc to stop...')
    
    keyboard.wait("f", suppress=True)

    commands["stop"] = escape
    frames=[]
    recording = False
    with mic as source:
        while running:
            buffer = source.stream.read(source.CHUNK)
            frames.append(buffer)
            if recording:
                if len(frames) > 50: 
                    frame_str = b"".join(frames[-20:])
                    arr = np.abs(np.frombuffer(frame_str, np.int16))
                    if arr.max() < min_noise_level:
                        print_sl('finished recording, procesing...')
                        frame_str = b"".join(frames)
                        frame_data = sr.AudioData(frame_str, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                        res = translate(frame_data)
                        clear_terminal_line()
                        if res["status"]:
                            callback(res["msg"])
                        recording = False
                        frames = []
            elif len(frames)>10:
                frame_str = b"".join(frames[-10:])
                arr = np.abs(np.frombuffer(frame_str, np.int16))
                if arr.max() > min_noise_level:
                    recording = True
                    print_sl("recording")
                elif len(frames) > 30:
                    frames = frames[-30:]

def act(msg):
    phrase_arr = msg.split(" ")
    is_command = False
    for (key, func) in commands.items():
        try:
            idx = phrase_arr.index(key)
            is_command = True
            func(phrase_arr[idx:])
            break
        except ValueError:
            continue

    if not is_command:
        tts(msg)

if __name__ == "__main__":
    print("Starting...")
    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if "USB PnP" in mic_name:
            device_index=mic_index
            print("mic chosen: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)
    
    looped_listen(main_mic, act)
