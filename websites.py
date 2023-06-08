import webbrowser as web
from tts_functions import tts
import json
import psutil

path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
def open_site(phrase):
    # check if chrome is open
    #"chrome.exe" in (i.name() for i in psutil.process_iter())
    #choose website to open
    dest = None
    f = open('secrets\sites.json')
    data = json.load(f)
    try:
        dest = data[phrase[0]]
    except Exception as e:
        print("Website not recognized.\n" + str(e))
        return
    try:
        print("Opening " + dest)
        web.get(path).open(dest)
    except Exception as e:
        print("Error: " + str(e))