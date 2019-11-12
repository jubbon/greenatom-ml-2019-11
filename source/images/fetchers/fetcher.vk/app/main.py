#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver


def fetch(user_vk_id: str):
    '''
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.set_window_size(1920, 1024)
    browser.maximize_window()
    browser.get(f"https://vk.com/{user_vk_id}")
    browser.implicitly_wait(10)  # seconds
    browser.save_screenshot(f"/data/screenshots/{user_vk_id}.png")
    browser.quit()


def main():
    '''
    '''
    import time
    while True:
        print("Fetching data from ВКонтакте", flush=True)
        fetch(user_vk_id="id19381401")
        time.sleep(60)
