import os
from assets.class_templates import command_module
from AppOpener import give_appnames, open as appopen 
import webbrowser as web
import json
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(__file__)),'secrets')


path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"browser_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)
path = path.replace('\\', '/') + " %s"

class module(command_module):
    def __init__(self):
        commands = {"open" : self.mopen,
                    "list apps" : self.list_apps}
        self.apps = give_appnames()
        super().__init__("Open Module", commands)
    
    def open_site(self, phrase_arr, vd):
        dest = None
        phrase = ' '.join(phrase_arr[1:])

        # load websites from json
        file_to_open = os.path.join(path_to_secrets,'sites.json')
        if os.path.isfile(file_to_open):
            f = open(file_to_open, 'r')
        else:
            f = open(os.path.join(path_to_secrets, 'sites_example.json'), 'r')
        data = json.load(f)
        f.close()

        try:
            dest = data[phrase]
        except KeyError as e:
            print("Website not recognized.\n" + str(e))
            return False
        try:
            vd.tts("Opening " + phrase)
            web.get(path).open(dest, new=2, autoraise=True)
        except Exception as e:
            print("Error: " + str(e))
            return False
        return True

    def open_app(self, phrase_arr, vd):
        app_name = ' '.join(phrase_arr[1:])
        if app_name in self.apps:
            vd.tts("Opening " + app_name)
            appopen(app_name)
            return True
        return False

    def list_apps(self, phrase_arr, vd):
        print(', '.join(list(self.apps)))
    
    def mopen(self, phrase_arr, vd):
        if not self.open_app(phrase_arr, vd):
            print(' '.join(pharse_arr[1:]) + " is not recognized as an app, checking if registered as website.")
            return self.open_site(phrase_arr, vd)
        return True
            
