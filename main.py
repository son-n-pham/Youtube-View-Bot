import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import proxy

WEBPAGE = "https://www.youtube.com/watch?v=ueGjwnifFck"

# Varied watching time from 30 to 50s to prevent Youtube algorithm to recognize the bot.
WATCH_TIME = random.randint(40, 60)

NUMBER_OF_BOTS = 2


def click_play(driver):
    try:
        player = driver.find_element(By.XPATH, '//*[@id="movie_player"]/div[4]/button')
        player.click()
        return True
    except Exception as e:
        print(e)
        driver.close()
        return False


def healthy_proxies():
    # Ensure having at least 3 proxy for web grapping

    while True:
        proxies_df = proxy.proxy_list_read()
        print(len(proxies_df.index))
        if len(proxies_df.index) < proxy.PROXIES_MIN_NUM:
            proxy.proxy_list_download(proxies_df)
        else:
            break

    return list(proxies_df["proxy"])


if __name__ == "__main__":

    bots = []

    used_proxies = []
    while len(bots) < NUMBER_OF_BOTS:

        proxies = healthy_proxies()
        proxy_no = len(proxies) - 1

        while proxy_no >= 0:
            try:
                # Refresh the bot during the time of starting other bots
                if len(bots)>0:
                    for bot in bots:
                        if time.time()-bot[1]>WATCH_TIME:
                            bot[0].refresh()
                            click_play(bots[0])

                current_proxy = proxies[proxy_no]
                if current_proxy not in used_proxies:
                    driver = proxy.open_webpage(WEBPAGE, proxies[proxy_no])
                    used_proxies.append(proxy_no)
                    if click_play(driver):
                        bots.append([driver, time.time()])
            except Exception as e:
                #print(e)
                print(f"{proxies[proxy_no]} is not working")
                proxies.pop(proxy_no)
            finally:
                proxy_no -= 1

        if proxy_no <= 0:
            proxy.proxies_to_csv([])
            proxies = healthy_proxies()

    while True:
        time.sleep(WATCH_TIME)
        for i in range(NUMBER_OF_BOTS):
            bots[i][0].refresh()
            click_play(bots[i])
