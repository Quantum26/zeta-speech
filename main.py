import speech_recognition as sr
import sys
sys.path.insert(1, '../')
from assets.tts_funcs import tts_engine
from assets.voice_driver import voice_driver
from apps.start_modules import load_modules

default_mic = "USB PnP"

if __name__ == "__main__":
    print("Starting...")

    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if default_mic in mic_name:
            device_index=mic_index
            print("Mic Selected: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)

    with tts_engine() as tts:
        tts.single_thread_mode()
        vd = voice_driver(mic=main_mic, tts=tts.tts)
        load_modules(vd)
        vd.run()
