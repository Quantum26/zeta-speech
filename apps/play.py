#from apps.chrome.youtube import YTDriver as youtube
from apps.chrome.selenium_yt import SeleniumYT

def yt_play(phrase_arr, tts):
    yt = youtube(phrase_arr[1:])
    yt.play()