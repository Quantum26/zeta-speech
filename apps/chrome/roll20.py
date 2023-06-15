from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import keyboard
import os
import time
import json
import sys
path_to_secrets = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'secrets')
sys.path.insert(1, path_to_secrets)
sys.path.insert(2, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import speech_recognition as sr
import pyaudio
from assets.tts_funcs import tts_engine
from scripts import selenium_start
from voice_driver import voice_driver


default_mic = "USB PnP"

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
        self.iframe = {}
        self.class_resource = None
        self.resource_left = None
        self.resource_right = None
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
    def open_char(self, name="Harthos"):
        self.open_characters()
        for charac in self.driver.find_elements(by=By.CLASS_NAME, value="namecontainer"):
            if name in charac.text:
                print(charac.text)
                charac.click()
                break
        time.sleep(0.1)
        for iframe in self.driver.find_elements(by=By.TAG_NAME, value="iframe"):
            if name in iframe.get_attribute("title"):
                self.iframe[name] = iframe
                self.driver.switch_to.frame(iframe)
                self.class_resource = self.driver.find_element(by=By.NAME, value="attr_class_resource")
                self.resource_left = self.driver.find_element(by=By.NAME, value="attr_resource_left")
                self.resource_right = self.driver.find_element(by=By.NAME, value="attr_resource_right")
                self.driver.switch_to.default_content()
                break

    def attack(self, weapon, char="Harthos"):
        self.open_chat()
        self.driver.switch_to.frame(self.iframe[char])
        for elem in self.driver.find_elements(by=By.NAME, value="roll_attack"):
            #p = elem.findElement(By.xpath("./.."))
            #c = elem.findElements(By.xpath("./child::*"))
            for c in elem.find_elements(by=By.NAME, value = "attr_atkname"):
                try:
                    if weapon in c.text:
                        elem.click()
                        if weapon=="Longbow":
                            quiver_arrows = int(self.resource_right.get_attribute("title"))
                            if quiver_arrows > 0:
                                self.resource_right.clear()
                                self.resource_right.send_keys(str(quiver_arrows-1))
                            else:
                                arrows = int(self.class_resource.get_attribute("title"))
                                if arrows > 0:
                                    self.class_resource.clear()
                                    self.class_resource.send_keys(str(arrows-1))
                        break
                except Exception as e:
                    print(e)
        self.driver.switch_to.default_content()

    def roll_damage(self):
        self.open_chat()
        messages = self.driver.find_elements(by=By.XPATH, value="//div[@class='message general you']")
        for index in range(len(messages)):
            elem = messages[-index-1]
            try:
                elem.find_element(by=By.TAG_NAME, value='a').click()
                break
            except NoSuchElementException:
                continue

    def roll_skill(self, skill_name, char="Harthos"):
        self.open_chat()
        self.driver.switch_to.frame(self.iframe[char])
        if skill_name == "animal":
            skill_name = "animal_handling"
        if skill_name == "sleight":
            skill_name = "sleight_of_hand"
        try:
            self.driver.find_element(by=By.NAME, value="roll_" + skill_name).click()
        except NoSuchElementException:
            pass
        self.driver.switch_to.default_content()

    def roll_save(self, skill_name, char="Harthos"):
        self.open_chat()
        self.driver.switch_to.frame(self.iframe[char])
        try:
            self.driver.find_element(by=By.NAME, value="roll_" + skill_name + "_save").click()
        except NoSuchElementException:
            pass
        self.driver.switch_to.default_content()


    def process_command(self, msg, tts=print):
        tts(msg)
        if "attack" in msg or "hit" in msg or "kaboom" in msg or "smack" in msg:
            if "short" in msg and "sword" in msg:
                self.attack(weapon = "Shortsword")
            elif "bow" in msg or "longbow" in msg:
                self.attack(weapon = "Longbow")
            elif "mall" in msg or "maul" in msg:
                self.attack(weapon = "Maul")
        elif "roll" in msg and "save" in msg:
            msg = msg.split(" ")
            self.roll_save(msg[msg.index("save")-1])
        elif "roll" in msg and "damage" in msg:
            self.roll_damage()
        elif "roll" in msg:
            msg = msg.split(" ")
            self.roll_skill(msg[msg.index("roll")+1])

if __name__ == "__main__":
    #selenium_start()
    # with roll20_driver() as d:
    #     time.sleep(3)
    #     d.open_char("Harthos")
    #     while True:
    #         input1 = input()
    #         if input1() == "quit":
    #             break
    #         d.process_command(input1)
    print("Starting...")

    device_index = 1
    for mic_index, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        if default_mic in mic_name:
            device_index=mic_index
            print("mic chosen: " + mic_name)
            break
    main_mic = sr.Microphone(device_index=device_index)
    with roll20_driver() as d:
        time.sleep(3)
        d.open_char("Harthos")
        with tts_engine() as tts:
            vd = voice_driver(mic=main_mic, commands={}, tts=tts.tts)
            vd.looped_listen(callback=lambda msg : d.process_command(msg))