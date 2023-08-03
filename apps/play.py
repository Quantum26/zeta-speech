from apps.chrome.youtube import SeleniumYoutube
from apps.chrome.yt_music import SeleniumYTMusic
from apps.open import selenium_start
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from subprocess import Popen
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(__file__)),'secrets')

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"chrome\\chrome_path.txt"), 'r') as f:
        chrome_path = f.read()
except Exception as e:
    print(e)


def music_play(phrase_arr, vd):
    print("starting selenium driver")
    music = SeleniumYTMusic()
    music_key = vd.add_local_object(music)
    play_func = vd.remove_commands(["music play"])[0]
    def music_stop(*args):
        music.stop()
        vd.remove_commands(["music"], prefix=True)
        vd.add_commands({"music play": play_func})
        vd.rm_local_object(music_key)
    vd.run_on_exit({"music stop": music_stop})
    vd.add_commands({
        "music play next" : lambda st, vd: music.add_to_queue(st[2:]),
        "music play" : lambda st, vd: music.play(st[2:]),
        "music pause" : lambda st, vd: music.pause(),
        "music unpause" : lambda st, vd: music.unpause(),
        "music back" : lambda st, vd: music.prev(),
        "music previous" : lambda st, vd: music.prev(),
        "music skip" : lambda st, vd: music.next(),
        "music next" : lambda st, vd: music.next(),
        "music stop" : music_stop,
        "music add" : lambda st, vd: music.add_to_queue(st[2:]),
        "music toggle" : lambda st, vd: music.toggle_music_page(),
        "music repeat" : lambda st, vd: music.toggle_repeat(),
        "music search" : lambda st, vd: music.search(st[2:]),
        "music shuffle" : lambda st, vd: music.toggle_shuffle()
    })
    print("music started with key:" + music_key)
    print("playing " + " ".join(phrase_arr[2:]))
    music.play(phrase_arr[2:])

def yt_play(phrase_arr, vd):
    print("starting selenium driver")
    yt = SeleniumYoutube()
    yt_key = vd.add_local_object(yt)
    play_func = vd.remove_commands(["youtube play"])[0]
    def yt_stop(*args):
        yt.stop()
        vd.remove_commands(["youtube"], prefix=True)
        vd.add_commands({"youtube play": play_func})
        vd.rm_local_object(yt_key)
    vd.run_on_exit({"youtube stop": yt_stop})
    vd.add_commands({
        "youtube play" : lambda st, vd: yt.play(st[2:]),
        "youtube pause" : lambda st, vd: yt.pause(),
        "youtube unpause" : lambda st, vd: yt.unpause(),
        "youtube stop" : yt_stop,
        "youtube repeat" : lambda st, vd: yt.toggle_repeat(),
        "youtube search" : lambda st, vd: yt.search(st[2:]),
    })
    print("yt started with key:" + yt_key)
    print("playing " + " ".join(phrase_arr[2:]))
    yt.play(phrase_arr[2:])

class selenium_wrapper():
    def __init__(self):
        profile_data = os.path.join(path_to_secrets, "profile_data")
        Popen([ chrome_path, 
                "--remote-debugging-port=8989", 
                "--user-data-dir=" + profile_data
                ], 
                shell=True, stdin=None, stdout=None, stderr=None)
        co = ChromeOptions()
        co.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options = co)
        print("Selenium started")
    def __enter__(self):
        self.__init__()
        return self
    def stop(self):
        print("Quitting Selenium")
        self.driver.quit()
    def __exit__(self, type, value, traceback):
        self.stop()
