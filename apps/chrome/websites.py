import webbrowser as web
import json
import psutil
import os

path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
def open_site(phrase):
    # check if chrome is open
    os.startfile("C:/Users/ianso/Desktop/ian.lnk")
    #choose website to open
    dest = None
    f = open(os.path.join(os.path.dirname(__file__), 'secrets/sites.json'), 'r')
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
    
    