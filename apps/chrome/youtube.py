from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import keyboard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')

class SeleniumYoutube():
    def __init__(self, driver=None):
        if driver is None:
            co = ChromeOptions()
            co.add_experimental_option("debuggerAddress", "localhost:8989")
            self.driver = webdriver.Chrome(options = co)
        else:
            self.driver = driver
        self.on_search_page = False
        self.paused = True

    def __enter__(self, driver=None):
        self.__init__(driver=driver)
        return self

    def stop(self):
        self.pause()
        print("Quitting Selenium Driver")
        self.driver.quit()

    def __exit__(self, type, value, traceback):
        self.stop()

    def play(self, search_terms = []):
        if type(search_terms) != list:
            search_terms = search_terms.split(' ')
        if len(search_terms) == 0:
            self.unpause()
            return
        if not self.paused:
            self.pause()
        index_to_play = 1
        if self.on_search_page and search_terms[0].isdigit():
            index_to_play = int(search_terms[0])
            if index_to_play <= 0:
                index_to_play = 1
        else:
            self.search(search_terms, play=True)
        results = self.driver.find_element(by=By.ID, value="primary").find_elements(by=By.TAG_NAME, value="ytd-video-renderer")
        if len(results) < index_to_play:
            index_to_play = len(results)
        results[index_to_play-1].click()
        self.paused = False

    def search(self, search_terms, play=False):
        if type(search_terms) != list:
            search_terms = search_terms.split(' ')
        URL = "https://youtube.com/results?search_query=" + '+'.join(search_terms)
        if not play:
            print("say 'youtube play' + an index of what video to play in results. (i.e. \"youtube play 1\")")
        self.driver.get(URL)
        self.on_search_page = True

    def __call__(self, search_terms):
        self.play(search_terms)
    def unpause(self):
        if self.paused:
            self.paused = False
    def pause(self):
        if not self.paused:
            self.paused = True
    def refresh():
        self.driver.refresh()

if __name__ == "__main__":
    print("x")
