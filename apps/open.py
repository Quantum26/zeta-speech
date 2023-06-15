from apps.chrome.websites import open_site
from apps.discord import open_discord

def open_app(phrase_arr, tts):
    if "discord" in phrase_arr:
        tts("Opening discord!")
        open_discord()
    else:
        open_site(phrase_arr[1:])
