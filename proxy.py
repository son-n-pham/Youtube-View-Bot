# This is to replace the manual download of ChromeDriver by using webdriver_manager
# selenium.webdriver.chrome.service is used as the previous version of directly referring ChromeDriver is depreciated
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

PROXIES_FILE = "proxies.csv" # file to save list of proxies
PROXIES_MIN_NUM = 3 # minimum number of proxies in the list
NUMBER_OF_BOT = 3 # number of bots
TIMEOUT = 120 # parameter of timeout for selenium to connect to the desired web
WEBPAGE = "https://www.youtube.com/watch?v=hL_chrFfJxY"


def open_webpage(webpage, proxy=None):
    if proxy is not None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_page_load_timeout(TIMEOUT)
    driver.get(webpage)
    return driver


def proxies_to_csv(proxies, proxies_file=PROXIES_FILE):
    if isinstance(proxies, pd.DataFrame):
        proxies.to_csv(proxies_file, index=False)
    elif isinstance(proxies, list):
        pd.DataFrame.from_dict({"proxy": proxies}).to_csv(proxies_file, index=False)
    else:
        print("This function can save only DataFram or list to csv file.")


def proxy_list_read(proxy_file=PROXIES_FILE):
    # Read proxies.csv or create the empty proxies.csv if that file does not exist
    # Return df DataFrame as the result
    try:
        df = pd.read_csv(proxy_file)
        print(f"{PROXIES_FILE} exists")
    except FileNotFoundError:
        print(f"Create new {PROXIES_FILE}")
        proxies_to_csv([])
        df = proxy_list_read()

    return df


def proxy_list_download(df, proxy_web="https://free-proxy-list.net/"):
    df = proxy_list_read()

    driver = open_webpage(proxy_web)

    proxy_rows = driver.find_elements(By.CSS_SELECTOR, ".table tbody tr")

    proxies_added_count = 0

    row_count = 0
    for row in proxy_rows:
        row_count += 1
        proxy_row = row.find_elements(By.CSS_SELECTOR, "td")
        try:
            proxy = f"{proxy_row[0].text}:{proxy_row[1].text}"
            if proxy not in list(df["proxy"]):
                df = df.append({"proxy": proxy}, ignore_index=True)
                print(f"{proxy} was added into {PROXIES_FILE}")
                proxies_added_count += 1
        except IndexError:
            print(f"{proxies_added_count} proxies were added into the proxies.csv file.")
            break

    print(df.head())

    proxies_to_csv(df)

    driver.close()


if __name__ == "__main__":

    # Ensure having at least 3 proxy for web grapping
    while True:
        proxies_df = proxy_list_read()
        print(len(proxies_df.index))
        if len(proxies_df.index) < PROXIES_MIN_NUM:
            proxy_list_download(proxies_df)
        else:
            break
