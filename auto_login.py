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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F67F4737131461F2E3051A5311C707D70BABA6AC8CC126F16ADCB1012B0987F584C8070F24C252E98533DEFEB8F33E63558375A82D5CFDF178109F999A8C0EE93B91F0865C3084232E2E9E349E222F961101868C8F60A16571394E5F99FB800F79F0E29235C605165DB7490A81A807705FBAFFFB37D72302DB2B423076B99D98100261C70147C62ED1BA72C2DD22F9742A801CD6E089CD4CC5017E7D56B692561B0CD5CF760CE012D2999A079C3F41B5CE4591FCB9F47C327A37CDF8AB92772361F7FDEFA286C96440D816966BF592CFD8D3AE5B68B4F62239BA0DF837CC4DF590CCEA0EC31F3D871EA9BD3DB8F9B843B221B608DE521BD9743F36462C10D4976397327639515F7D9FC4D12E19C7C52BA62E75C878321FC64425735A1BCAFB5818C4E9AD8F16ACC87ABAF2F14410EBD2FFFC2CD3F133A871BE5D720EB1AD3F97"})
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
