from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import keyboard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from assets.class_templates import command_module

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')

class SeleniumYTMusic(command_module):
    def __init__(self, driver=None, window_handle = None):
        


        if driver is None:
            co = ChromeOptions()
            co.add_experimental_option("debuggerAddress", "localhost:8989")
            self.driver = webdriver.Chrome(options = co)
        else:
            self.driver = driver
        if window_handle is None:
            self.window_handle = self.driver.window_handles[-1]
        else:
            self.window_handle = window_handle
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
        URL = "https://music.youtube.com/search?q=" + '+'.join(search_terms)
        self.driver.get(URL)
        time.sleep(1)
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading ']")))
        try:
            self.driver.find_element(by=By.XPATH, value="//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading ']").click()
            self.paused = False
        except Exception as e:
            print("ran into problems: " + e)

    def search(self, search_terms):
        if type(search_terms) != list:
            search_terms = search_terms.split(' ')
        search_bar = self.driver.find_element(by=By.CLASS_NAME, value="search-box")
        search_bar.click()
        search_bar = search_bar.find_element(by=By.TAG_NAME,value="input")
        search_bar.clear()
        search_bar.send_keys(' '.join(search_terms))
        search_bar.send_keys('\n')

    def add_to_queue(self, search_terms):
        print("Adding '" + " ".join(search_terms) + "' to play next!")
        self.search(search_terms)
        time.sleep(5)
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "button-shape")))
        self.driver.find_element(by=By.ID, value="button-shape").click()
        for option in self.driver.find_elements(by=By.TAG_NAME, value="ytmusic-menu-service-item-renderer"):
            if option.find_element(by=By.TAG_NAME, value="yt-formatted-string").text == "Play next":
                option.click()

    def __call__(self, search_terms):
        self.play(search_terms)
    def toggle_music_page(self):
        self.driver.find_element(by=By.CLASS_NAME, value="middle-controls").click()
    def unpause(self):
        if self.paused:
            self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.CLASS_NAME, value="play-pause-button").click()
            self.paused = False
    def pause(self):
        if not self.paused:
            try:
                self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.CLASS_NAME, value="play-pause-button").click()
            except Exception as e:
                print("Issue with pausing: " + e)
            self.paused = True
    def prev(self):
        self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.XPATH, value="//tp-yt-paper-icon-button[@title='Previous']").click()
    def next(self):
        self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.XPATH, value="//tp-yt-paper-icon-button[@title='Next']").click()
    def toggle_repeat(self):
        self.driver.find_element(by=By.ID, value="expand-repeat").click()
    def toggle_shuffle(self):
        self.driver.find_element(by=By.ID, value="expand-shuffle").click()
    def refresh():
        self.driver.refresh()

if __name__ == "__main__":
    with SeleniumYTMusic() as youtube_music:
        keyboard.add_hotkey("space", callback=youtube_music.pause, suppress=True)
        keyboard.add_hotkey("e", callback=lambda : youtube_music.add_to_queue("crossing field lisa"), suppress=True) 
        # keyboard.add_hotkey("n", callback=youtube_music.next, suppress=True)
        # keyboard.add_hotkey("p", callback=youtube_music.prev, suppress=True)
        youtube_music("cupid by fifty fifty".split(" "))
        keyboard.wait('esc', suppress=True)
