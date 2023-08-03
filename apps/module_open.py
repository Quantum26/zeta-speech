import os
from assets.class_templates import command_module
from AppOpener import give_appnames, open as appopen 

path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"browser_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)

class module(command_module):
    def __init__(self):
        commands = {"open" : self.open_app}
        self.apps = give_appnames()
        super().__init__("Open Module", commands)

    def open_app(self, phrase_arr, voice_driver):
        app_name = ' '.join(phrase_arr[1:])
        if app_name in self.apps:
            voice_driver.tts("Opening " + app_name)
            appopen(app_name)
        else:
            print(app_name + " is not in apps.")
