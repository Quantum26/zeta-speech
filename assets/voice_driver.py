import speech_recognition as sr
import pyaudio
from assets.tts_funcs import tts_engine
from assets.console import print_sl, clear_terminal_line
from assets.class_templates import command_module
import numpy as np
import keyboard

class voice_driver():
    def __init__(self, mic : sr.Microphone, commands = {}, min_noise_level = 3500, tts=print):
        self.default_commands = {
            "list commands" : self.list_commands,
            "quit" : self.escape,
            "exit": self.escape,
            "tts on" : lambda *args: self.set_tts(True),
            "tts off" : lambda *args: self.set_tts(False),
            "set" : self.set_flag,
            }        
        self.commands = commands
        self.r = sr.Recognizer()
        self.mic = mic
        self.min_noise_level = min_noise_level
        self.min_voice_frame_count = 50
        self.min_frame_count = 10
        self.tts = tts
        self.tts_on = True
        self.commands.update(self.default_commands)
        self.module_index = -1
        self.modules = {}
        self.flag_dict = {}

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
    
    def set_tts(self, val):
        self.tts_on = val
        self.tts("TTS set to " + str(val))

    def add_module(self, m : command_module):
        self.commands.update(m.get_commands())
        self.module_index += 1
        idx = self.module_index
        self.modules[idx] = (m)
        for flag in m.get_flag_names():
            self.flag_dict[flag] = idx
        return idx

    def remove_module(self, idx : int, run_exit_funcs=True):
        if idx not in self.modules:
            return {
                "status_ok" : False,
                "msg" :  "Module does not exist."
            }
        for key in self.modules[idx].get_commands().keys():
            self.commands.pop(key)
        for flag in self.modules[idx].get_flag_names():
            self.flag_dict.pop(flag)
        status_msg = "Removed module successfully."
        if run_exit:
            status_msg = "Removed and " + self.modules[idx].exit()
        return {
                "status_ok" : True,
                "msg" : status_msg,
                "module" :  self.modules.pop(idx)
            }
    def list_commands(self, *args):
        print("Here are the commands:")
        for cmd in self.commands.keys():
            print(cmd)
    def set_flag(self, phrase_arr, voice_driver):
        name = phrase_arr[0]
        value = phrase_arr[1]
        if name in self.flag_dict:
            self.modules[self.flag_dict[name]].set_flag(value)
            self.tts("Flag " + name + " set to " + str(value))
        else:
            print("Could not set flag: " + name)

    def escape(self, *args):
        print("Exiting Modules")
        for module in self.modules.values():
            print(module.exit())
        print("quitting...")
        self.running = False

    def looped_listen(self, callback = print):
        self.running = True

        keyboard.add_hotkey('shift+esc', callback=self.escape, suppress=False)

        self.commands.update(self.default_commands)

        frames=[]
        self.recording = False

        print('started! press shift + esc or say "quit" or "exit" to quit')
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
        commands = self.commands.items()
        for (key, func) in commands:
            key = key.split(" ")
            try:
                idx = phrase_arr.index(key[0])
                is_command = True
                for i in range(1, len(key)):
                    if key[i] != phrase_arr[idx+i]:
                        is_command = False
                        break
                if is_command:
                    success = func(phrase_arr[idx:], self)
                    break
            except ValueError:
                is_command = False
                continue
            except IndexError:
                is_command = False
                continue

        if not is_command:
            if self.tts_on:
                self.tts(msg)
            else:
                print("Command not recognized: " + msg)
    def run(self):
        self.looped_listen(self.act)