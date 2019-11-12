from selenium import webdriver


def fetch(user_ok_id: str):
    '''
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_window_size(1920, 1024)
    browser.maximize_window()
    browser.get(f"https://ok.ru/profile/{user_ok_id}")
    browser.implicitly_wait(10)  # seconds
    browser.save_screenshot(f"/data/screenshots/{user_ok_id}.png")
    browser.quit()


def main():
    '''
    '''
    import time
    while True:
        print("Fetching data from Одноклассники", flush=True)
        fetch(user_ok_id="561773297648")
        time.sleep(60)
