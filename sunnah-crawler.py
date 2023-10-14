import browserDriver
import crawler
import time

from log import LOG

print("Start")
browser_driver_instance = browserDriver.BrowserDriver(LOG)
driver = browser_driver_instance.get_browser_driver()
crawler_instance = crawler.Crawler(LOG, driver, "bukhari", 5)
crawler_instance.visit_page()
print("end")


time.sleep(5000)