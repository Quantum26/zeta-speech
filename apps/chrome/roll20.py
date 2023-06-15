from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pygame import mixer
import keyboard
import os
import json
import sys
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')
sys.path.insert(1, path_to_secrets)
from scripts import selenium_start

class roll20_driver():
    def start_roll20(self):
        co = ChromeOptions()
        co.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options = co)
        with open(os.path.join(path_to_secrets,'sites.json'), 'r') as f:
            links_data = json.load(f)
        URL = links_data["prima"]
        self.driver.get(URL)
        self.chat = self.driver.find_element(By.ID, "ui-id-1")
        self.characters = self.driver.find_element(By.ID, "ui-id-3")
        self.char = None
    def __enter__(self):
        self.start_roll20()
        return self
    def __exit__(self, type, value, traceback):
        print("goodbye")
        self.driver.quit()
    def refresh(self):
        self.driver.refresh()
    def open_characters(self):
        self.characters.click()
    def open_chat(self):
        self.chat.click()
    def attack(self, weapon, char="Harthos"):
        for elem in self.driver.find_elements(by=By.Name, value="roll_attack"):
            p = elem.findElement(By.xpath("./.."))
            

    

if __name__ == "__main__":
    selenium_start()
    with roll20_driver() as d:
        keyboard.wait('esc', suppress=True)