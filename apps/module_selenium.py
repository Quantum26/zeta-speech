import webbrowser as web
import os
from assets.class_templates import command_module
from apps.chrome.yt_music import SeleniumYTMusic
from subprocess import Popen
from threading import Thread
from time import sleep

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(__file__)),'secrets')

path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"browser_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)


class module(command_module):
    def __init__(self):
        commands = {"open selenium" : self.selenium_start,
                    "play" : self.play}
        super().__init__("Selenium Module", commands)
    
    def selenium_start(self, phrase_arr, vd):
        profile_data = os.path.join(path_to_secrets, "profile_data")
        os.makedirs(profile_data, exist_ok=True)
        def st_cmd():
            Popen([ path, 
                    "--remote-debugging-port=8989", 
                    "--user-data-dir=" + profile_data
                    ], 
                    shell=True, stdin=None, stdout=None, stderr=None)
        t = Thread(target = st_cmd)
        t.start()
        sleep(0.5)
        return True
    def music_play(self, phrase_arr, vd):
        music = SeleniumYTMusic()
        index = vd.add_module(music)
        print("playing " + " ".join(phrase_arr[1:]))
        music.play(phrase_arr[1:])
        def music_quit(*args):
            vd.remove_module(index) 
            vd.remove_commands(["quit music", "exit music"])
            vd.add_commands({"play" : self.play})
        vd.add_commands({
            "quit music" : music_quit,
            "exit music" : music_quit,
        })
        return True
    def play(self, phrase_arr, vd):
        self.music_play(phrase_arr, vd)
        return True
    
    