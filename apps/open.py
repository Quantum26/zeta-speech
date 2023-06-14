from apps.chrome.websites import open_site
from apps.discord import open_discord
from assets.tts_funcs import tts

def open_app(phrase_arr):
    if "discord" in phrase_arr:
        tts("Opening discord! awdoisfjoijjfwlaklk")
        open_discord()
    else:
        open_site(phrase_arr[1:])
