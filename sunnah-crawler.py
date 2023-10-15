# project
import browserDriver
import crawler
import driverOperations
import hadithParser
from log import LOG
from helpers import is_error, quit_app_with_wait

# python
from colorama import Fore
from colorama import Style

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

chapter_no, chapter_name = hadith_parser_instance.parse_chapter_no_and_name()
print(Fore.CYAN + "chapter_no" + Style.RESET_ALL)
print(chapter_no)
print(Fore.CYAN + "chapter_name" + Style.RESET_ALL)
print(chapter_name)

english_hadith_narrated_text, english_hadith_details_text = hadith_parser_instance.parse_english_text()
print(Fore.CYAN + "english_hadith_narrated_text" + Style.RESET_ALL)
print(english_hadith_narrated_text)
print(Fore.CYAN + "english_hadith_details_text" + Style.RESET_ALL)
print(english_hadith_details_text)

reference_dict = hadith_parser_instance.parse_reference()
print(Fore.GREEN + "reference_dict" + Style.RESET_ALL)
print(reference_dict)


print("Press any key to exit...")
input()
driver.quit()
driver.close()
print("Key pressed")