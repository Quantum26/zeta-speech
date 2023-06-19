from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
import keyboard
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')

class SeleniumYT():
    def __enter__(self):
        co = ChromeOptions()
        co.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options = co)
        return self
    def __exit__(self, type, value, traceback):
        self.driver.quit()
    def __call__(self, search_terms):
        URL = "https://music.youtube.com/search?q=" + '+'.join(search_terms)
        self.driver.get(URL)
        elem = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "yt-button-shape")))
        self.driver.find_element(by=By.TAG_NAME, value="yt-button-shape").click()
    def pause(self):
        self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.CLASS_NAME, value="play-pause-button").click()
    def prev(self):
        self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.XPATH, value="//tp-yt-paper-icon-button[@title='Previous']").click()
    def next(self):
        self.driver.find_element(by=By.ID, value="left-controls").find_element(by=By.XPATH, value="//tp-yt-paper-icon-button[@title='Next']").click()
    def refresh():
        self.driver.refresh()

if __name__ == "__main__":
    with SeleniumYT() as youtube_music:
        youtube_music("cupid by fifty fifty".split(" "))
        keyboard.wait('esc', suppress=True)
