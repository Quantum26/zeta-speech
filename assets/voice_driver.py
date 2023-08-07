import speech_recognition as sr
import pyaudio
from assets.tts_funcs import tts_engine
from assets.console import print_sl, clear_terminal_line
import numpy as np
import keyboard

class voice_driver():
    def __init__(self, mic : sr.Microphone, commands = {}, min_noise_level = 3500, tts=print):
        self.default_commands = {
            "list commands" : self.list_commands,
            "set tts on" : lambda *args: self.set_tts(True),
            "set tts off" : lambda *args: self.set_tts(False),
            "quit" : self.escape,
            "exit": self.escape,
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
        self.exit_funcs = {}
        self.local_objects = {}
        self.obj_index = 0

    def translate(self, audio):
        """ Speech-to-text helper function. 
        Use to change speech-to-text API.
        
        Input: Audio file to translate
        Output: Response packet with status and translation/error fields. 
        """
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

    def sort_commands(self):
        """Makes sure longer commands are first in command dictionary.
            This way commands like "set tts" take priority over the default "set".
        """
        temp_commands = self.commands
        self.commands = {}
        for k in sorted(temp_commands.keys(), key=len, reverse=True):
            self.commands[k] = temp_commands[k]

    def set_tts(self, val):
        self.tts_on = val

    def add_commands(self, cmds):
        self.commands.update(cmds)
        self.sort_commands()
        
    def remove_commands(self, keywords : list, prefix = False):
        result = []
        for key in keywords:
            if prefix:
                keys_to_remove = []
                for cmd_key in self.commands.keys():
                    if key == cmd_key.split(' ')[0]:
                        keys_to_remove.append(cmd_key)
                #print(keys_to_remove)
                for rm_key in keys_to_remove:
                    result.append(self.commands.pop(rm_key))
                    #print("key removed: " + rm_key)
            else:
                    result.append(self.commands.pop(key))
        return result

    def set_commands(self, cmds):
        self.commands = cmds
        self.commands.update(self.default_commands)
        self.sort_commands()
    
    def add_local_object(self, o, key=None):
        if key is None:
            key = str(self.obj_index)
            self.obj_index += 1
        self.local_objects[key] = o
        return key
    
    def rm_local_object(self, key):
        try:
            return self.local_objects.pop(key)
        except KeyError:
            print("key not in local objects")
            return None

    def run_on_exit(self, entry):
        """ Add functions that need to be run on exit for clean finishes.
            This requires the keyword to be a command at exit.
            Please try to avoid using this unless absolutely necessary.
        Args:
            entry (dict): {keyword : function to be run}
        """
        self.exit_funcs.update(entry)

    def escape(self, *args):
        print("checking for exit functions to run")
        for (key,value) in self.exit_funcs.items():
            if key in self.commands.keys():
                try:
                    value()
                except Exception as e:
                    print(e)
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
        command_found = False
        success = True
        for (start_idx, end_idx, func) in self.get_commands_to_run(phrase_arr):
            command_found = True
            if not func(phrase_arr[start_idx:end_idx], self):
                success = False
        if not success or not command_found:
            if self.tts_on:
                self.tts(msg)
            else:
                print("Command not recognized: " + msg)

    def get_commands_recurs(phrase_arr):
        if len(phrase_arr) == 0:
            return []
        commands = self.commands.items()
        results = []
        for (key,func) in commands:
            key = key.split(" ")
            try:
                idx = phrase_arr.index(key[0])
                is_command = True
                for i in range(1, len(key)):
                    if key[i] != phrase_arr[idx+i]:
                        is_command = False
                        break
                if is_command:
                    results.extend(self.get_commands_to_run(phrase_arr[:idx]))
                    results.append((idx, func))
                    results.extend(self.get_commands_to_run(phrase_arr[idx+len(key):]))
                    break
            except ValueError:
                continue
            except IndexError:
                continue
        return results
    def get_commands_to_run(pharse_arr):
        results = get_commands_recurs(pharse_arr)
        for i in range(len(results)):
            if i < len(results)-1:
                results[i] = (results[i][0], results[i+1][0], results[1])
            else:
                results[i] = (results[i][0], len(phrase_arr), results[1])
        return results
        
    def run(self):
        self.looped_listen(self.act)