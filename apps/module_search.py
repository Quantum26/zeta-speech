import webbrowser as web
import os
from assets.class_templates import command_module

path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"browser_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)
path = path.replace('\\', '/') + " %s"


class module(command_module):
    def __init__(self):
        commands = {"search" : self.google_search}
        super().__init__("Search Module", commands)
    def google_search(self, phrase, voice_driver):
        if len(phrase) == 1:
            print("Sorry I didn't catch that. Try Googling again.")
        dest = "https://www.google.com/search?q=" + "+".join(phrase[1:])
        try:
            print("Googling \"" + " ".join(phrase[1:]) + "\".")
            web.get(path).open(dest, 2)
        except Exception as e:
            print("Error: " + str(e))
    
    