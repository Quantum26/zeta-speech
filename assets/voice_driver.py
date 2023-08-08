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
            "list flags" : self.list_flags,
            "quit" : self.escape,
            "exit": self.escape,
            "set" : self.set_flag,
            }        
        self.commands = commands
        self.add_commands(self.default_commands)
        self.r = sr.Recognizer()
        self.mic = mic
        self.min_noise_level = min_noise_level
        self.min_voice_frame_count = 50
        self.min_frame_count = 10
        self.tts_cmd = tts
        self.module_index = -1
        self.modules = {}
        self.flag_dict = {"tts" : True, "repeat" : True}

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
            If a command has two words, with the first one matching a default command,
            the two word command takes priority.
        """
        temp_commands = self.commands
        self.commands = {}
        for k in sorted(temp_commands.keys(), key=len, reverse=True):
            self.commands[k] = temp_commands[k]

    def add_commands(self, new_commands):
        """Adds commands and makes sure longer commands are first in command dictionary.
            If a command has two words, with the first one matching a default command,
            the two word command takes priority.
        """
        temp_commands = self.commands
        temp_commands.update(new_commands)
        self.commands = {}
        for k in sorted(temp_commands.keys(), key=len, reverse=True):
            self.commands[k] = temp_commands[k]
        #self.list_commands()

    def remove_commands(self, keywords : list):
        result = []
        for key in keywords:
            result.append(self.commands.pop(key))
        return result

    def tts(self, msg):
        if self.flag_dict["tts"]:
            self.tts_cmd(msg)
        else:
            print(msg)

    def add_module(self, m : command_module):
        """Adds a command module to the driver, adding its commands, flags, and will run
        the command module's exit function on exiting.

        Args:
            m (command_module): Command module to add.

        Returns:
            int: The index of the module for remove_module.
        """
        self.add_commands(m.get_commands())
        self.module_index += 1
        idx = self.module_index
        self.modules[idx] = (m)
        for flag in m.get_flag_names():
            self.flag_dict[flag] = idx
        return idx

    def remove_module(self, idx : int, run_exit_funcs=True):
        """Removes a module from the voice driver.

        Args:
            idx (int): Index from add_module to remove the module.
            run_exit_funcs (bool, optional): If set to True, runs command module's exit function. Defaults to True.

        Returns:
            {
                'status_ok' (bool): True if module was removed. 
                'msg' (str): Message with information about removal.
                'module' (command_module): The module that was removed (if it was removed successfully).
            }
        """
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
        if run_exit_funcs:
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
        return True

    def list_flags(self, *args):
        print("Here are the flags:")
        print(" | ".join(self.flag_dict.keys()))
        return True

    def set_flag(self, phrase_arr, voice_driver):
        name = phrase_arr[1]
        value = bool("true" in phrase_arr[2:] or "on" in phrase_arr[2:])

        if name in self.flag_dict:
            if type(self.flag_dict[name]) == int:
                self.modules[self.flag_dict[name]].set_flag(name, value)
            else:
                self.flag_dict[name] = value
            self.tts(name + " set to " + str(value))
            return True
        else:
            print("Could not set " + name)
            return False

    def escape(self, *args):
        print("Exiting Modules")
        for module in self.modules.values():
            print(module.exit())
        print("quitting...")
        self.running = False
        return True

    def looped_listen(self, callback = print):
        self.running = True

        keyboard.add_hotkey('shift+esc', callback=self.escape, suppress=False) # suppress=True breaks terminal?

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
        if self.flag_dict["repeat"]:
            self.tts(msg)
        elif not success or not command_found:
            print("Command not recognized: " + msg)

    def get_commands_recurs(self, phrase_arr):
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
                    results.extend(self.get_commands_recurs(phrase_arr[:idx]))
                    results.append((idx, func))
                    results.extend(self.get_commands_recurs(phrase_arr[idx+len(key):]))
                    break
            except ValueError:
                continue
            except IndexError:
                continue
        return results
    def get_commands_to_run(self, phrase_arr):
        results = self.get_commands_recurs(phrase_arr)
        for i in range(len(results)):
            if i < len(results)-1:
                results[i] = (results[i][0], results[i+1][0], results[i][1])
            else:
                results[i] = (results[i][0], len(phrase_arr), results[i][1])
        return results
        
    def run(self):
        self.looped_listen(self.act)