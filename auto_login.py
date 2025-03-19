# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BB113DF7AAC48DBD9D21275F6D8B1720CD58C57F2B031D3CCC0392D7AD0D9438D68F0BFB27AFB7611F00F356752E6D330BDAD637B0786B1DD9BE5581D247AB4C522BA949B0812FA5F7EF91F20C01235C5AB58A4D1B3955F011E39F452988D48EEC2E388B1181F747E4C5FB11C6BF7A03AA74756788F883DA8074648321A95EDAA106D3AD35E0C7B010F2C5502371BDB4567699E63E0FD38AE0AD6DEE5134FBAD0DA8BA2DB26539511E17FFDF14A2B4C6A596ADBC2ABA7C29205578EA1B43F2FE6A97B481A9003F1F69D3D1EC6468E52EAF5FB6AB7AA519078EDBAFC848919054DA5AA37FF7836E2020F1A6801C5CB9A8FAB15543E98494BC1FC0E5F1B294D2169E7A2D1D21E8D617098AF8D356727FB560D247D9DCB8F6573F4CE3855E0D50D225CEB16E4EF3B04414F9C37A9737BF154F2A2A030901C81B0A510395383DFA5FA1D47AD653C58DE04EC1EE657D60991788CF84B2EB76C54EA1FCC04CDE3A9AFE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
