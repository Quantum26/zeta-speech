from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from subprocess import Popen
import os

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(__file__)),'secrets')

class command_module():
    def __init__(self, name : str, commands = {}, flags = {}, objs = {}, exit_funcs=[]):
        self.name = name
        self.commands = commands
        self.flags = flags
        self.objs = objs
        self.exit_funcs = exit_funcs
    def get_commands(self):
        return self.commands
    def add_commands(self, cmds):
        self.commands.update(cmds)
    def remove_commands(self, keywords : list):
        result = []
        for key in keywords:
            result.append(self.commands.pop(key))
        return result
    def set_flag(self, name : str, val : bool):
        self.flags[name] = val
    def get_flag(self, name : str):
        try:
            flag_val = self.flags[name]
            return {
                "flag_exists": True,
                "flag": flag_val
            }
        except:
            return {
                "flag_exists": False
            }
    def get_flag_names(self):
        return self.flags.keys()
    def exit(self):
        exit_msg = "Exited " + self.name
        err = False
        for func in self.exit_funcs:
            try:
                func()
            except Exception as e:
                if not err:
                    exit_msg += " with Exceptions: " + str(e)
                    err = True
                else: 
                    exit_msg += ", " + str(e)
        return exit_msg


class selenium_module(command_module):
    def __init__(self, name="Selenium Module", commands = {}, flags = {}, objs = {}, exit_funcs={}):
        profile_data = os.path.join(path_to_secrets, "profile_data")
        Popen([ chrome_path, 
                "--remote-debugging-port=8989", 
                "--user-data-dir=" + profile_data
                ], 
                shell=True, stdin=None, stdout=None, stderr=None)
        co = ChromeOptions()
        co.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options = co)

        exit_funcs["selenium_exit"] = self.stop
        super().__init__(name, commands, flags, objs, exit_funcs)
        print("Started selenium Driver for" + name)
    def __enter__(self):
        self.__init__()
        return self
    def stop(self, *args):
        print("Quitting Selenium Driver for " + self.name)
        self.driver.quit()
    def __exit__(self, type, value, traceback):
        self.stop()