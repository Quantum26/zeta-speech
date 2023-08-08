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
        commands = {"open" : self.multi_open,
                    "list apps" : self.list_apps}
        flags = {"start" : False}
        self.apps = give_appnames()
        super().__init__("Open Module", commands, flags=flags)
    
    def open_site(self, phrase_arr, vd, recognized_msg=True):

        # check if chrome is open
        if self.flags["start"] and os.path.isfile(os.path.join(path_to_secrets,"chrome_profile.lnk")):
            os.startfile(os.path.join(path_to_secrets,"chrome_profile.lnk"))
            self.flags["start"] = False

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
            if recognized_msg:
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
    
    def multi_open(self, phrase_arr, vd):
        for name in ' '.join(phrase_arr[1:]).split('and'):
            sub_arr = ["open"]
            sub_arr.extend(name.split())
            if len(sub_arr) == 1:
                continue
            if not self.open_app(sub_arr, vd) and not self.open_site(sub_arr, vd, False):
                print(' '.join(sub_arr[1:]) + " is not recognized as an app or website.")
        return True
            
