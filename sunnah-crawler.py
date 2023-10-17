# project
import browserDriver
import crawler
import driverOperations
import hadithParser
import elementList
import database
from log import LOG
from helpers import is_error, quit_app_with_wait
from hadith import Hadith, ChapterInfo, Text, EnglishText, ArabicText, Reference, HadithProcessor

# python
import json
from colorama import Fore
from colorama import Style

print("Starting sunnah crawler....")
browser_driver_instance = browserDriver.BrowserDriver(LOG)
driver = browser_driver_instance.get_browser_driver()
if is_error(driver):
    quit_app_with_wait(LOG, driver)


crawler_instance = crawler.Crawler(LOG, driver)
response = crawler_instance.visit_page("bukhari", 5)
if is_error(driver):
    quit_app_with_wait(LOG, response)


driver_operation_instance = driverOperations.DriverOperations(driver, LOG)
hadith_parser_instance = hadithParser.HadithParser(driver_operation_instance, LOG)

chapter_no, chapter_name = hadith_parser_instance.parse_chapter_no_and_name()
if is_error(chapter_no):
    quit_app_with_wait(LOG, chapter_no, driver)
print(Fore.CYAN + "chapter_no" + Style.RESET_ALL)
print(chapter_no)
print(Fore.CYAN + "chapter_name" + Style.RESET_ALL)
print(chapter_name)

english_hadith_narrated_text, english_hadith_details_text = hadith_parser_instance.parse_english_text()
if is_error(english_hadith_narrated_text):
    quit_app_with_wait(LOG, english_hadith_narrated_text)
print(Fore.CYAN + "english_hadith_narrated_text" + Style.RESET_ALL)
print(english_hadith_narrated_text)
print(Fore.CYAN + "english_hadith_details_text" + Style.RESET_ALL)
print(english_hadith_details_text)

reference_dict = hadith_parser_instance.parse_reference()
if is_error(reference_dict):
    quit_app_with_wait(LOG, reference_dict)
print(Fore.GREEN + "reference_dict" + Style.RESET_ALL)
print(reference_dict)


arabic_text = hadith_parser_instance.parse_arabic_text()
if is_error(arabic_text):
    quit_app_with_wait(LOG, arabic_text)
print(Fore.CYAN + "arabic_text" + Style.RESET_ALL)
print(arabic_text)

# Creating a full Hadith object
chapter_info = ChapterInfo(chapter_no=chapter_no, chapter_name=chapter_name)
english_text = EnglishText(narrated_text=english_hadith_narrated_text, details_text=english_hadith_details_text)
arabic_text = ArabicText(full_arabic_text=arabic_text)
text = Text(english_text=english_text, arabic_text=arabic_text)
reference = Reference(reference=reference_dict[elementList.reference], in_book_reference=reference_dict[elementList.in_book_reference], uscmsa_web_reference=reference_dict[elementList.uscmsa_web_reference])


hadith = Hadith(chapter_info=chapter_info, reference=reference, text=text)
print("Hadith:")
print(hadith.pprint_str())

hadith_processor = HadithProcessor()
hadith_json = hadith_processor.hadith_to_json(hadith)
print("json length::")
print(len(hadith_json))

print("string json to db")
db_instance = database.Database(LOG)
db_instance.create_database()

insert = db_instance.insert_data(hadith.chapter_info.chapter_no + "+" + hadith.chapter_info.chapter_name + "+" + hadith.reference.reference, hadith_json)
print("insert")
print(insert)


get = db_instance.get_data(hadith.chapter_info.chapter_no + "+" + hadith.chapter_info.chapter_name + "+" + hadith.reference.reference)
print("get")
print(get)

# database value to object
hadith_object_recreated_from_db = hadith_processor.json_to_hadith(hadith_json=get)
print("hadith_object_recreated_from_db")
print(hadith_object_recreated_from_db.pprint_str())

delete = db_instance.delete_data(hadith.chapter_info.chapter_no + "+" + hadith.chapter_info.chapter_name + "+" + hadith.reference.reference)
print("delete")
print(delete)

#### JSON to object
hadith_object_recreated = hadith_processor.json_to_hadith(hadith_json=hadith_json)
print("hadith_object_recreated")
print(hadith_object_recreated.pprint_str())


print("are the two strings equal?")
print(hadith.pprint_str() == hadith_object_recreated.pprint_str())

print("Press any key to exit...")
input()
driver.quit()
# driver.close()
print("Key pressed")