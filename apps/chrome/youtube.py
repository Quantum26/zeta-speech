import sys
import argparse
import requests
from googlesearch import search
import webbrowser as web
import json
import urllib
from bs4 import BeautifulSoup
import re
import os

path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
try:
    with open(os.path.join(os.path.dirname(__file__),"chrome_path.txt"), 'r') as f:
        path = f.read()
except Exception as e:
    print(e)

class YTDriver:
    def __init__(self, search_terms):
        self.prev_results = self.google_search(search_terms)

    def play_top_result(self):
        self.play(self.prev_results[0])

    def play(self, video_id):
        api_key="AIzaSyCndqlWOOnsXS-czeo9nGf-XmSfHocVKUQ"
        searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+video_id+"&key="+api_key+"&part=contentDetails"
        response = urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        all_data=data['items']
        contentDetails=all_data[0]['contentDetails']
        duration=contentDetails['duration']
        print(duration[2:])

    def google_search(self, search_terms):
        try:
            return [result.split('=')[1] for result in search("youtube music " + ' '.join(search_terms), num=5, stop=5, pause=2)]
        except Exception as e:
            print("Error: " + str(e))
            return


if __name__ == "__main__":
    response = urllib.request.urlopen('https://www.twitch.tv/sliggytv/videos').read()
    soup = BeautifulSoup(response, features='html.parser')
    res = str(response)
    print([res[m.start():m.start()+16] for m in re.finditer('videos/', res)])
    # print(soup.prettify())
    # print(soup.find('script').text)
    # search_terms = sys.argv[1:]
    # music = YTDriver(search_terms)
    # music.play_top_result()
