import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

WEBPAGE = "https://www.youtube.com/watch?v=ueGjwnifFck"

# Varied watching time from 30 to 50s to prevent Youtube algorithm to recognize the bot.
WATCH_TIME = random.randint(40, 60)

NUMBER_OF_DRIVERS = 1


def click_play(driver):
    try:
        player = driver.find_element(By.XPATH, '//*[@id="movie_player"]/div[4]/button')
        player.click()
    except Exception as e:
        print(e)


drivers = []
# ChromeDriverManager is used to automatically download ChromeWebdriver
for i in range(NUMBER_OF_DRIVERS):
    drivers.append(webdriver.Chrome(service=Service(ChromeDriverManager().install())))
    drivers[i].get(WEBPAGE)
    click_play(drivers[i])

while True:
    time.sleep(WATCH_TIME)
    for i in range(NUMBER_OF_DRIVERS):
        drivers[i].refresh()
        click_play(drivers[i])
