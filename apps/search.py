import webbrowser as web
import os

path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

def google_search(phrase, tts):
    if len(phrase) == 1:
        print("Sorry I didn't catch that. Try Googling again.")
    dest = "https://www.google.com/search?q=" + "+".join(phrase[1:])
    try:
        print("Googling \"" + " ".join(phrase[1:]) + "\".")
        web.get(path).open(dest)
    except Exception as e:
        print("Error: " + str(e))
    
    