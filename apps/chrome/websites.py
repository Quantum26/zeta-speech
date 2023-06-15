import webbrowser as web
import json
import os
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')
path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

def open_site(phrase, start=False):
    # check if chrome is open
    if start and os.path.isfile(os.path.join(path_to_secrets,"ian.lnk")):
        os.startfile(os.path.join(path_to_secrets,"ian.lnk"))
    #choose website to open
    dest = None
    file_to_open = os.path.join(path_to_secrets,'sites.json')
    if os.path.isfile(file_to_open):
        f = open(file_to_open, 'r')
    else:
        f = open(os.path.join(path_to_secrets, 'sites_example.json'), 'r')

    data = json.load(f)
    f.close()
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
    
    