# project
import browserDriver
import crawler
import driverOperations
import hadithParser
import elementList
import databaseHadith
import databaseHadithLink
import commonVariables
from log import LOG
from helpers import is_error, quit_app_with_wait, parse_hadith_reference
from hadith import Hadith, BookInfo, ChapterInfo, Text, Link, EnglishText, ArabicText, Reference, HadithProcessor

# python
import json
import time
import logging
from colorama import Fore
from colorama import Style
import sys


# Creating hadith DB instance
LOG.post_log("Creating hadith DB instance....", logging.INFO)
hadith_db_instance = databaseHadith.DatabaseHadith(LOG)
hadith_db_instance.create_database()
LOG.post_log("Successfully created hadith DB instance..", logging.INFO)
time.sleep(3)

# Creating hadith processor
LOG.post_log("Creating hadith processor....", logging.INFO)
hadith_processor = HadithProcessor()
LOG.post_log("Successfully created hadith processor..", logging.INFO)
time.sleep(3)

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

# get all data
hadith_keys, hadith_values  = hadith_db_instance.get_all_data()
# print("total len")
# print(len(hadith_keys))


# filtered keys
# counter = 0
# hadith_filtered_keys = []
# for hadith_key in hadith_keys:
#     print(hadith_key)
#     counter = counter + 1
#     if counter > 10:
#         break


# Creating link DB instance
LOG.post_log("Creating link DB instance....", logging.INFO)
link_db_instance = databaseHadithLink.DatabaseHadithLink(LOG)
link_db_instance.create_database()
LOG.post_log("Successfully created link DB instance..", logging.INFO)
time.sleep(3)

# get all data
link_keys, link_values  = link_db_instance.get_all_data()
# print("total len")
# print(len(link_keys))


# filtered keys
# counter = 0
# link_filtered_keys = []
# for link_key in link_keys:
#     print(link_key)
#     counter = counter + 1
#     if counter > 10:
#         break


print("total hadiths recorded: {}, total links recorded: {}".format(len(hadith_keys), len(link_keys)))

print("creating hadith record map")
hadith_key_map = {}
for hadith_key in hadith_keys:
    hadith_key_map[hadith_key] = True

print("creating hadith link map")
link_key_map = {}
for link_key in link_keys:
    link_key_map[link_key] = True


# print("LINK MAP")
# print(link_key_map)

## Which one exists as a link but not hadith?
counter = 0
absent_hadiths = []
for link in link_keys:
    if link not in hadith_key_map:
        if counter < 10:
            print("{} does not exist in the hadith record".format(link))
        absent_hadiths.append(link)
        counter = counter + 1


print("Hadiths that do not exists in record:")
print(absent_hadiths)
print(len(absent_hadiths))

print("Returning here for the moment")
sys.exit(0)


# Let's see how many we can resolve just by directly going to the website
counter = 0
for link in absent_hadiths:
    book, number = parse_hadith_reference(link)
    print("Book: {}, number: {}".format(book, number))

    response = crawler_instance.visit_to_hadith_page(book, number)
    counter = counter + 1
    # if counter > 10:
    #     break

    ###################
    ###################
    LOG.post_log("Trying to insert to database directly for book: {}, number: {}".format(book, number), logging.INFO)
    time.sleep(10)
    # Prepare hadith payload
    try:
        book_no, book_name = hadith_parser_instance.parse_book_no_and_name()
        if is_error(book_no) or is_error(book_name):
            # quit_app_with_wait(LOG, book_no + commonVariables.separator + book_name)
            LOG.post_log("Ignoring hadith with book: {} and number: {} because of error".format(book, number), logging.ERROR)
            continue

        chapter_no, chapter_name = hadith_parser_instance.parse_chapter_no_and_name()
        if is_error(chapter_no) or is_error(chapter_name):
            # quit_app_with_wait(LOG, chapter_no + commonVariables.separator + chapter_name)
            LOG.post_log("Ignoring hadith with book: {} and number: {} because of error".format(book, number), logging.ERROR)
            continue

        english_hadith_narrated_text, english_hadith_details_text = hadith_parser_instance.parse_english_text()
        if is_error(english_hadith_narrated_text) or is_error(english_hadith_details_text):
            # quit_app_with_wait(LOG, english_hadith_narrated_text + commonVariables.separator + english_hadith_details_text)
            LOG.post_log("Ignoring hadith with book: {} and number: {} because of error".format(book, number), logging.ERROR)
            continue
        
        reference_dict = hadith_parser_instance.parse_reference()
        if is_error(reference_dict):
            # quit_app_with_wait(LOG, reference_dict)
            LOG.post_log("Ignoring hadith with book: {} and number: {} because of error".format(book, number), logging.ERROR)
            continue
        
        arabic_text = hadith_parser_instance.parse_arabic_text()
        if is_error(arabic_text):
            # quit_app_with_wait(LOG, arabic_text)
            LOG.post_log("Ignoring hadith with book: {} and number: {} because of error".format(book, number), logging.ERROR)
            continue

        page_url = driver_operation_instance.get_page_url()
        
        # Creating a full Hadith object
        book_info = BookInfo(book_no=book_no, book_name=book_name)
        chapter_info = ChapterInfo(chapter_no=chapter_no, chapter_name=chapter_name)
        english_text = EnglishText(narrated_text=english_hadith_narrated_text, details_text=english_hadith_details_text)
        arabic_text = ArabicText(full_arabic_text=arabic_text)
        text = Text(english_text=english_text, arabic_text=arabic_text)
        link = Link(url=page_url)
        reference = Reference(reference=reference_dict[elementList.reference], in_book_reference=reference_dict[elementList.in_book_reference], uscmsa_web_reference=reference_dict[elementList.uscmsa_web_reference])

        print("parsed reference: {}".format(reference))
        hadith = Hadith(book_info=book_info, chapter_info=chapter_info, reference=reference, text=text, link=link)
        hadith_json = hadith_processor.hadith_to_json(hadith)

        # Get the hadith grade
        hadith_grade = hadith_parser_instance.get_hadith_grade(book)

        print("for insert. hadith reference is")
        print(hadith.reference.reference)
        time.sleep(3)
        insert = hadith_db_instance.insert_data(hadith.reference.reference, hadith_json, hadith_grade)
        if insert is False:
            quit_app_with_wait(LOG, "Failed to insert hadith into DB")
        

        LOG.post_log("Inserted hadith successfully with chapter no: {}, chapter name: {}, reference: {}".format(hadith.chapter_info.chapter_no, hadith.chapter_info.chapter_name, reference.reference), logging.INFO)
    except ValueError:
        LOG.post_log("Trying to insert data directly failed with book: '{}', number: '{}'".format(book, number), logging.DEBUG)#
    # time.sleep(1)
    ###################
    ###################