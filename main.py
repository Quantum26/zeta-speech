import speech_recognition as sr
import pyaudio
import sys
sys.path.insert(1, '../')
from assets.tts_funcs import tts_engine
from assets.console import print_sl, clear_terminal_line
from apps.search import google_search
from apps.open import open_app, set_start
from apps.play import music_play, yt_play
from assets.voice_driver import voice_driver
import numpy as np
import keyboard
from threading import Thread

commands = {
    "open" : open_app,
    "music play" : music_play,
    "youtube play" : yt_play,
    "set start" : set_start,
    "google" : google_search,
    "start" : open_app,
}

default_mic = "USB PnP"

if __name__ == "__main__":
    print("Starting...")

    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if default_mic in mic_name:
            device_index=mic_index
            print("mic chosen: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)

    with tts_engine() as tts:
        tts.single_thread_mode()
        vd = voice_driver(mic=main_mic, commands=commands, tts=tts.tts)
        vd.run()
