import webbrowser as web
import json
import os
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')

path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"chrome_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)
path = path.replace('\\', '/') + " %s"

def open_site(phrase, start=False):
    # check if chrome is open
    if start and os.path.isfile(os.path.join(path_to_secrets,"chrome_profile.lnk")):
        os.startfile(os.path.join(path_to_secrets,"chrome_profile.lnk"))
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
        dest = data[phrase]
    except KeyError as e:
        try:
            dest = data[phrase.split(' ')[0]]
        except KeyError:
            print("Website not recognized.\n" + str(e))
            return False
    try:
        print("Opening " + dest)
        web.get(path).open(dest)
    except Exception as e:
        print("Error: " + str(e))
        return False
    return True
    