from apps.chrome.websites import open_site
from apps.discord import open_discord
import os
import sys
from threading import Thread
from time import sleep
from subprocess import Popen
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(__file__)),'secrets')
sys.path.insert(1, path_to_secrets)

chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"chrome\\chrome_path.txt"), 'r') as f:
        chrome_path = f.read()
except Exception as e:
    print(e)

global start
start = False

def set_start(phrase_arr, vd):
    global start
    if "true" in phrase_arr:
        vd.tts("start set to True")
        start = True
    elif "false" in phrase_arr:
        vd.tts("start set to False")
        start = False

def selenium_start():
    profile_data = os.path.join(path_to_secrets, "profile_data")
    os.makedirs(profile_data, exist_ok=True)
    def st_cmd():
        Popen([ chrome_path, 
                "--remote-debugging-port=8989", 
                "--user-data-dir=" + profile_data], 
                shell=True, stdin=None, stdout=None, stderr=None)
    t = Thread(target = st_cmd)
    t.start()
    sleep(0.5)
    
open_dict = [
        {"key":"discord" ,"msg":"Opening Discord!", "func":open_discord}, 
        {"key":"selenium" ,"msg":"Opening Selenium Browser!", "func":selenium_start}
        ]
def open_app(phrase_arr, voice_driver):
    global start
    for app_dict in open_dict:
        if phrase_arr[1]==app_dict["key"]:
            if app_dict["msg"] is not None:
                voice_driver.tts(app_dict["msg"])
            app_dict["func"]()
            return
    if open_site(' '.join(phrase_arr[1:]), start):
        if start:
            start = False
