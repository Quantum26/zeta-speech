import webbrowser as web
import os
from assets.class_templates import command_module

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
        commands = {"open selenium" : self.selenium_start}
        super().__init__("Selenium Module", commands)
    
    def selenium_start(self, phrase_arr, vd):
        profile_data = os.path.join(path_to_secrets, "profile_data")
        os.makedirs(profile_data, exist_ok=True)
        def st_cmd():
            Popen([ chrome_path, 
                    "--remote-debugging-port=8989", 
                    "--user-data-dir=" + profile_data
                    ], 
                    shell=True, stdin=None, stdout=None, stderr=None)
        t = Thread(target = st_cmd)
        t.start()
        sleep(0.5)
        return True
    
    