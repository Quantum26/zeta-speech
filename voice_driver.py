import speech_recognition as sr
import pyaudio
from assets.tts_funcs import tts_engine
from assets.console import print_sl, clear_terminal_line
import numpy as np
import keyboard

class voice_driver():
    def __init__(self, mic : sr.Microphone, commands = {}, min_noise_level = 3500, tts=print):
        self.commands = commands
        self.r = sr.Recognizer()
        self.mic = mic
        self.min_noise_level = min_noise_level
        self.min_voice_frame_count = 50
        self.min_frame_count = 10
        self.tts = tts

    """ Speech-to-text helper function. 
        Use to change speech-to-text API.
        
        Input: Audio file to translate
        Output: Response packet with status and translation/error fields. 
        """
    def translate(self, audio):
        response = {
            "status": True,
            "msg" : None
        }
        try:
            response["msg"] = self.r.recognize_google(audio).lower()
        except sr.RequestError:
            response["status"] = False
            response["msg"] = "API unavailable"
        except sr.UnknownValueError:
            response["status"] = False
            response["msg"] = "Speech Unrecognizable"
        return response

    def listen(self):
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            print("listening")
            audio = self.r.listen(mic)
        response = self.translate(audio)
        return response

    def looped_listen(self, callback = print):
        self.running = True

        def escape(*args):
            print("quitting...")
            self.running = False
        keyboard.add_hotkey('esc', callback=escape, suppress=True)

        print('started! press esc or say "quit" or "exit" to quit')

        self.commands["quit"] = escape
        self.commands["exit"] = escape

        frames=[]
        self.recording = False
        with self.mic as source:
            while self.running:
                buffer = source.stream.read(source.CHUNK)
                frames.append(buffer)
                if self.recording:
                    if len(frames) > self.min_voice_frame_count: 
                        frame_str = b"".join(frames[-3*self.min_frame_count:])
                        arr = np.abs(np.frombuffer(frame_str, np.int16))
                        if arr.max() < self.min_noise_level:
                            print_sl('finished recording, processing...')
                            frame_str = b"".join(frames)
                            frame_data = sr.AudioData(frame_str, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                            res = self.translate(frame_data)
                            clear_terminal_line()
                            if res["status"]:
                                callback(res["msg"])
                            self.recording = False
                            frames = []
                elif len(frames)>self.min_frame_count:
                    frame_str = b"".join(frames[-self.min_frame_count:])
                    arr = np.abs(np.frombuffer(frame_str, np.int16))
                    if arr.max() > self.min_noise_level:
                        self.recording = True
                        print_sl("recording")
                    elif len(frames) > 3*self.min_frame_count:
                        frames = frames[-3*self.min_frame_count:]

    def act(self, msg):
        phrase_arr = msg.split(" ")
        is_command = False
        for (key, func) in self.commands.items():
            key = key.split(" ")
            try:
                idx = phrase_arr.index(key[0])
                is_command = True
                for i in range(1, len(key)):
                    if key[i] != phrase_arr[idx+i]:
                        is_command = False
                        break
                if is_command:
                    func(phrase_arr[idx:], self.tts)
                    break
            except ValueError:
                is_command = False
                continue
            except IndexError:
                is_command = False
                continue

        if not is_command:
            self.tts(msg)
    def run(self):
        self.looped_listen(self.act)