# project
import browserDriver
import crawler
import driverOperations
import hadithParser
import elementList
import databaseHadith
import commonVariables
from log import LOG
from helpers import is_error, quit_app_with_wait
from hadith import Hadith, BookInfo, ChapterInfo, Text, Link, EnglishText, ArabicText, Reference, HadithProcessor

# python
import json
import time
import logging
from colorama import Fore
from colorama import Style

LOG.post_log("Starting sunnah crawler....", logging.INFO)

# Browser
LOG.post_log("Creating browser instance....", logging.INFO)
browser_driver_instance = browserDriver.BrowserDriver(LOG)
driver = browser_driver_instance.get_browser_driver()
if is_error(driver):
    quit_app_with_wait(LOG, driver)
LOG.post_log("Successfully created browser instance..", logging.INFO)
time.sleep(3)


# Driver operation instance
LOG.post_log("Creating driver operation instance....", logging.INFO)
driver_operation_instance = driverOperations.DriverOperations(driver, LOG)
if is_error(driver_operation_instance):
    quit_app_with_wait(LOG, driver_operation_instance)
LOG.post_log("Successfully created driver operation instance..", logging.INFO)
time.sleep(3)


# Crawler
LOG.post_log("Creating crawler instance....", logging.INFO)
crawler_instance = crawler.Crawler(LOG, driver, driver_operation_instance)
if is_error(crawler_instance):
    quit_app_with_wait(LOG, crawler_instance)
LOG.post_log("Successfully created crawler instance..", logging.INFO)
time.sleep(3)


# Hadith parser instance
LOG.post_log("Creating hadith parser instance....", logging.INFO)
hadith_parser_instance = hadithParser.HadithParser(driver_operation_instance, LOG)
if is_error(hadith_parser_instance):
    quit_app_with_wait(LOG, hadith_parser_instance)
LOG.post_log("Successfully created hadith parser instance..", logging.INFO)
time.sleep(3)

# Creating DB instance
LOG.post_log("Creating DB instance....", logging.INFO)
db_instance = databaseHadith.DatabaseHadith(LOG)
db_instance.create_database()
LOG.post_log("Successfully created DB instance..", logging.INFO)
time.sleep(3)

# Creating hadith processor
LOG.post_log("Creating hadith processor....", logging.INFO)
hadith_processor = HadithProcessor()
LOG.post_log("Successfully created hadith processor..", logging.INFO)
time.sleep(3)

# Take in input for crawler
LOG.post_log("Enter hadith book....", logging.INFO)
hadith_book = input()
if hadith_book not in commonVariables.sunnah_book_list:
    quit_app_with_wait(LOG, "Hadith book name '{}' is invalid".format(hadith_book))
LOG.post_log("Hadith book name '{}' is valid".format(hadith_book), logging.INFO)
time.sleep(3)

LOG.post_log("Enter starting hadith number....", logging.INFO)
hadith_no_int = None
try:
    # Convert it into integer
    hadith_no = input()
    hadith_no_int = int(hadith_no)
except ValueError:
    LOG.post_log("Hadith book no '{}' is not a number. but continuing".format(hadith_no), logging.DEBUG)
    hadith_no_int = hadith_no
LOG.post_log("Hadith book no '{}' is valid".format(hadith_no_int), logging.INFO)
time.sleep(3)

LOG.post_log("Enter limit....", logging.INFO)
hadith_limit_int = None
try:
    # Convert it into integer
    hadith_limit = input()
    hadith_limit_int = int(hadith_limit)
except ValueError:
    quit_app_with_wait(LOG, "Hadith limit '{}' is invalid".format(hadith_limit))
LOG.post_log("Hadith limit '{}' is valid".format(hadith_limit_int), logging.INFO)
time.sleep(3)


# Printing wanring sign to proceed
LOG.post_log("Proceeding with crawling in ten seconds...", logging.DEBUG)
time.sleep(10)


LOG.post_log("Crawling hadiths....", logging.INFO)
for counter in range(hadith_limit_int):
    response = None
    if counter == 0:
        response = crawler_instance.visit_to_hadith_page(hadith_book, hadith_no_int)
    else:
        response = crawler_instance.go_to_next_page()
    
    if is_error(response):
        quit_app_with_wait(LOG, response)
    
    # Prepare hadith payload
    book_no, book_name = hadith_parser_instance.parse_book_no_and_name()
    if is_error(book_no) or is_error(book_name):
        quit_app_with_wait(LOG, book_no + commonVariables.separator + book_name)

    chapter_no, chapter_name = hadith_parser_instance.parse_chapter_no_and_name()
    if is_error(chapter_no) or is_error(chapter_name):
        quit_app_with_wait(LOG, chapter_no + commonVariables.separator + chapter_name)

    english_hadith_narrated_text, english_hadith_details_text = hadith_parser_instance.parse_english_text()
    if is_error(english_hadith_narrated_text) or is_error(english_hadith_details_text):
        quit_app_with_wait(LOG, english_hadith_narrated_text + commonVariables.separator + english_hadith_details_text)
    
    reference_dict = hadith_parser_instance.parse_reference()
    if is_error(reference_dict):
        quit_app_with_wait(LOG, reference_dict)
    
    arabic_text = hadith_parser_instance.parse_arabic_text()
    if is_error(arabic_text):
        quit_app_with_wait(LOG, arabic_text)

    page_url = driver_operation_instance.get_page_url()
    
    # Creating a full Hadith object
    book_info = BookInfo(book_no=book_no, book_name=book_name)
    chapter_info = ChapterInfo(chapter_no=chapter_no, chapter_name=chapter_name)
    english_text = EnglishText(narrated_text=english_hadith_narrated_text, details_text=english_hadith_details_text)
    arabic_text = ArabicText(full_arabic_text=arabic_text)
    text = Text(english_text=english_text, arabic_text=arabic_text)
    link = Link(url=page_url)
    reference = Reference(reference=reference_dict[elementList.reference], in_book_reference=reference_dict[elementList.in_book_reference], uscmsa_web_reference=reference_dict[elementList.uscmsa_web_reference])


    hadith = Hadith(book_info=book_info, chapter_info=chapter_info, reference=reference, text=text, link=link)
    hadith_json = hadith_processor.hadith_to_json(hadith)

    # Get the hadith grade
    hadith_grade = hadith_parser_instance.get_hadith_grade(hadith_book)

    insert = db_instance.insert_data(hadith.reference.reference, hadith_json, hadith_grade)
    if insert is False:
        quit_app_with_wait(LOG, "Failed to insert hadith into DB")
    

    LOG.post_log("Inserted hadith successfully with chapter no: {}, chapter name: {}, reference: {}".format(hadith.chapter_info.chapter_no, hadith.chapter_info.chapter_name, reference.reference), logging.INFO)
    time.sleep(3)

    ## LOG.post_log("Hadith details.....", logging.DEBUG)
    # retrieved_hadith = db_instance.get_data(hadith.chapter_info.chapter_no + "+" + hadith.chapter_info.chapter_name + "+" + hadith.reference.reference)
    # retrieved_hadith_obj = hadith_processor.json_to_hadith(hadith_json=retrieved_hadith)
    # LOG.post_log(retrieved_hadith_obj.pprint_str(), logging.DEBUG)
    # time.sleep(5)


print("Process complete. Press any key to exit...")
input()
driver.quit()



########################################################################################
## Extra for debugging

# print(Fore.CYAN + "chapter_no" + Style.RESET_ALL)
# print(chapter_no)
# print(Fore.CYAN + "chapter_name" + Style.RESET_ALL)
# print(chapter_name)


# print(Fore.CYAN + "english_hadith_narrated_text" + Style.RESET_ALL)
# print(english_hadith_narrated_text)
# print(Fore.CYAN + "english_hadith_details_text" + Style.RESET_ALL)
# print(english_hadith_details_text)


# print(Fore.GREEN + "reference_dict" + Style.RESET_ALL)
# print(reference_dict)


# print(Fore.CYAN + "arabic_text" + Style.RESET_ALL)
# print(arabic_text)


# print("Hadith:")
# print(hadith.pprint_str())


# hadith_json = hadith_processor.hadith_to_json(hadith)
# print("json length::")
# print(len(hadith_json))

# print("string json to db")




# # database value to object
# hadith_object_recreated_from_db = hadith_processor.json_to_hadith(hadith_json=get)
# print("hadith_object_recreated_from_db")
# print(hadith_object_recreated_from_db.pprint_str())

# delete = db_instance.delete_data(hadith.chapter_info.chapter_no + "+" + hadith.chapter_info.chapter_name + "+" + hadith.reference.reference)
# print("delete")
# print(delete)

# #### JSON to object
# hadith_object_recreated = hadith_processor.json_to_hadith(hadith_json=hadith_json)
# print("hadith_object_recreated")
# print(hadith_object_recreated.pprint_str())


# print("are the two strings equal?")
# print(hadith.pprint_str() == hadith_object_recreated.pprint_str())

# print("Press any key to exit...")
# input()
# driver.quit()
# # driver.close()
# print("Key pressed")