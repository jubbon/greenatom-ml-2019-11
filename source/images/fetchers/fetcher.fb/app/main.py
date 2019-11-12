from selenium import webdriver


def fetch(user_fb_id: str):
    '''
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_window_size(1920, 1024)
    browser.maximize_window()
    browser.get(f"https://web.facebook.com/{user_fb_id}")
    browser.implicitly_wait(10)  # seconds
    browser.save_screenshot(f"/data/screenshots/{user_fb_id}.png")
    browser.quit()


def main():
    '''
    '''
    import time
    while True:
        print("Fetching data from Facebook", flush=True)
        fetch(user_fb_id="aidar.saifoulline")
        time.sleep(60)
