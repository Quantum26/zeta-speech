from apps.chrome.websites import open_site
from apps.discord import open_discord

global start
start = False

def set_start(phrase_arr, tts):
    global start
    if "true" in phrase_arr:
        tts("start set to True")
        start = True
    elif "false" in phrase_arr:
        tts("start set to False")
        start = False

def open_app(phrase_arr, tts):
    global start
    if "discord" in phrase_arr:
        tts("Opening discord!")
        open_discord()
        phrase_arr.remove("discord")
    if len(phrase_arr)>1:
        open_site(phrase_arr[1:], start)
