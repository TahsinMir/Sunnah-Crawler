import browserDriver
import crawler

import time
import logging
import sys

from log import LOG
from helpers import is_error, quit_app_with_wait

print("Starting sunnah crawler....")
browser_driver_instance = browserDriver.BrowserDriver(LOG)
driver = browser_driver_instance.get_browser_driver()
if is_error(driver):
    quit_app_with_wait()


crawler_instance = crawler.Crawler(LOG, driver)
response = crawler_instance.visit_page("bukhari", 6)
if is_error(driver):
    quit_app_with_wait()


print("Press any key to exit...")
input()
print("Key pressed")