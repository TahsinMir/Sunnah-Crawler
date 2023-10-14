import os
import platform
import inspect
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import helpers
from commonVariables import errorPfx

class BrowserDriver:
    def __init__(self, logger):
        self.logger = logger
    def get_browser_driver(self):
        fn = helpers.get_function_name(inspect.currentframe())
        chrome_options = Options()

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920x1080')

        chrome_options.binary_location = get_chrome_application_location()

        driver = None
        errorMsg = None
        try:
            driver = webdriver.Chrome(options=chrome_options, service=Service(get_chromium_binary_location()))
            self.logger.post_log("{}: driver initialized".format(fn), logging.INFO)
        except Exception as e:
            if e is not None:
                errorMsg = self.logger.post_log("{}: {}: driver initialization failed, error: {}".format(errorPfx, fn, e), logging.ERROR)
                if driver is not None:
                    driver.close()
                    driver.quit()
                    driver = None
                return errorMsg
        return driver


def get_chrome_application_location():
    if platform.system() == "Windows":
        return "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    return "not implemented"

def get_chromium_binary_location():
    current_dir = os.getcwd()
    if platform.system() == "Windows":
        return current_dir + "\\" + "driver\\chromedriver-win64-118\chromedriver-win64\\chromedriver.exe"
    return "not implemented"
