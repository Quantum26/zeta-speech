import sys
sys.path.insert(1, '../')
import speech_recognition as sr
import pyaudio
from speech_recognition import AudioData
import matplotlib.pyplot as plt
import keyboard
from threading import Thread
import numpy as np
# import tkinter as ttk

# # root window
# root = ttk.Tk()
# root.geometry('300x200')
# root.resizable(False, False)
# root.title('Noise Gate')
# # slider current value
# current_value = ttk.DoubleVar(value = 50000)

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

def get_current_value():
    return int(current_value.get())

def looped_listen(mic : sr.Microphone, repeat=2):
    global running
    global plot
    global min_noise_level
    running = True
    plot = False
    min_noise_level = 4500
    # min_noise_level = get_current_value()

    # def slider_changed(event):
    #     min_noise_level = get_current_value()
    # slider = ttk.Scale(
    #     root,
    #     from_=30000,
    #     to=80000,
    #     orient='horizontal',
    #     variable=current_value,
    #     command=slider_changed
    # )
    # thread = Thread(target = root.mainloop)
    # thread.start()
    def plot_toggle():
        global plot
        plot = not plot
        output = "on" if plot else "off"
        print("plot toggled to " + output)
    def escape():
        global running
        print("esc pressed")
        running = False
    keyboard.add_hotkey('esc', callback=escape, suppress=True)
    print('press f to start, press esc to stop...')
    keyboard.wait("f", suppress=True)
    keyboard.add_hotkey('p', callback=plot_toggle, suppress=True)

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
                        print('finished recording, procesing...')
                        frame_str = b"".join(frames)
                        frame_data = AudioData(frame_str, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                        res = translate(frame_data)
                        if res["status"]:
                            print(res["msg"])
                        recording = False
                        frames = []
            elif len(frames)>10:
                frame_str = b"".join(frames[-10:])
                arr = np.abs(np.frombuffer(frame_str, np.int16))
                if arr.max() > min_noise_level:
                    recording = True
                    print("recording")
                elif len(frames) > 30:
                    frames = frames[-30:]
            
            if plot:
                frame_str = b"".join(frames)
                plt.plot(np.fromstring(frame_str, np.int16))
                plt.show()
                frame_data = AudioData(frame_str, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                print(translate(frame_data))
                plot = False

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
