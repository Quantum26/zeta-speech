import sys
sys.path.insert(1, '../')
import speech_recognition as sr
import pyaudio
from speech_recognition import AudioData
import matplotlib.pyplot as plt
import keyboard
from threading import Thread

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

def looped_listen(mic : sr.Microphone, repeat=2):
    frames=[]
    print('press f to start, press esc to stop...')
    keyboard.wait("f", suppress=True)
    running = True
    def escape():
        running = False
    keyboard.add_hotkey('esc', callback=escape, suppress=True)
    with mic as source:
        while running:
            buffer = source.stream.read(source.CHUNK)
            frames.append(buffer)
            if len(frames) > 100:
                frames = frames[1:]
                frame_data = AudioData(b"".join(frames), source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                if(False):
                    print(translate(frame_data))

if __name__ == "__main__":
    print("Starting...")
    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if "USB PnP" in mic_name:
            device_index=mic_index
            print("mic chosen: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)
    
    looped_listen(main_mic)
