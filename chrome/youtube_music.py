from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

def youtube_music(search_terms):
    co = ChromeOptions()
    co.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options = co)
    URL = "https://music.youtube.com/search?q=" + '+'.join(search_terms)
    try:
        driver.get(URL)
    except Exception as e:
        print("Error: " + str(e))
        return
    
    driver.quit()