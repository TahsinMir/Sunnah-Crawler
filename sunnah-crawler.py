# project
import browserDriver
import crawler
import driverOperations
import hadithParser
from log import LOG
from helpers import is_error, quit_app_with_wait

print("Starting sunnah crawler....")
browser_driver_instance = browserDriver.BrowserDriver(LOG)
driver = browser_driver_instance.get_browser_driver()
if is_error(driver):
    quit_app_with_wait(LOG, driver)


crawler_instance = crawler.Crawler(LOG, driver)
response = crawler_instance.visit_page("bukhari", 6)
if is_error(driver):
    quit_app_with_wait(LOG, response)


driver_operation_instance = driverOperations.DriverOperations(driver, LOG)
hadith_parser_instance = hadithParser.HadithParser(driver_operation_instance, LOG)

english_hadith_narrated_text, english_hadith_details_text = hadith_parser_instance.parse_english_text()
print("english_hadith_narrated_text")
print(english_hadith_narrated_text)
print("english_hadith_details_text")
print(english_hadith_details_text)

english_hadith_narrated_text = hadith_parser_instance.parse_reference()
print("english_hadith_narrated_text")
print(english_hadith_narrated_text)


print("Press any key to exit...")
input()
print("Key pressed")