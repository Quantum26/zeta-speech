from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import keyboard

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')

class SeleniumYT():
    def __enter__(self):
        co = ChromeOptions()
        co.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options = co)
        self.driver.get("https://music.youtube.com/")
        return self
    def __exit__(self, type, value, traceback):
        print("goodbye")
        self.driver.quit()
    def __call__(self, search_terms):
        URL = "https://music.youtube.com/search?q=" + '+'.join(search_terms)
        self.driver.get(URL)
    def refresh():
        self.driver.refresh()

if __name__ == "__main__":
    with SeleniumYT() as youtube_music:
        keyboard.wait("esc", suppress=True)
        youtube_music("cupid by fifty fifty".split(" "))
        keyboard.wait('esc', suppress=True)
