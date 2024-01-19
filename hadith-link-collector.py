# project
import browserDriver
import crawler
import driverOperations
import hadithParser
import elementList
import databaseHadithLink
import commonVariables
from log import LOG
from helpers import is_error, quit_app_with_wait
from commonVariables import errorPfx
from hadith import Hadith, BookInfo, ChapterInfo, Text, Link, EnglishText, ArabicText, Reference, HadithProcessor

# python
import json
import time
import logging
from colorama import Fore
from colorama import Style


LOG.post_log("Hadith link collector", logging.INFO)
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

# Creating DB instance
LOG.post_log("Creating DB instance....", logging.INFO)
db_instance = databaseHadithLink.DatabaseHadithLink(LOG)
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


LOG.post_log("Enter starting book number....", logging.INFO)
hadith_book_no_int = None
try:
    # Convert it into integer
    hadith_book_no = input()
    hadith_book_no_int = int(hadith_book_no)
except ValueError:
    LOG.post_log("Hadith book no '{}' is not a number. but continuing".format(hadith_book_no), logging.DEBUG)
    hadith_book_no_int = hadith_book_no
LOG.post_log("Hadith book no '{}' is valid".format(hadith_book_no_int), logging.INFO)
time.sleep(3)


LOG.post_log("Enter limit....", logging.INFO)
hadith_limit_int = None
try:
    # Convert it into integer
    hadith_limit = input()
    hadith_limit_int = int(hadith_limit)
except ValueError:
    quit_app_with_wait(LOG, "Hadith book limit '{}' is invalid".format(hadith_limit))
LOG.post_log("Hadith book limit '{}' is valid".format(hadith_limit_int), logging.INFO)
time.sleep(3)


# Printing wanring sign to proceed
LOG.post_log("Proceeding with crawling in ten seconds...", logging.DEBUG)
time.sleep(10)

LOG.post_log("Crawling hadiths links....", logging.INFO)
for counter in range(hadith_book_no_int, hadith_limit_int + 1):
    LOG.post_log("going to book no: {}".format(counter), logging.DEBUG)
    response = crawler_instance.go_to_hadith_book(hadith_book, counter)
    
    if is_error(response):
        quit_app_with_wait(LOG, response)
    

    LOG.post_log("Successfully parsed page", logging.INFO)
    time.sleep(5)

    try:
        full_reference_element = driver_operation_instance.get_elements_by_class(elementList.hadith_reference)
    except Exception as e:
        full_reference_element = None
    
    if is_error(full_reference_element) or full_reference_element is None:
        LOG.post_log("{}: error occured while getting page element list, error: {}".format(errorPfx, e), logging.ERROR)
        continue

    all_references = []
    for element in full_reference_element:
        element_array = driver_operation_instance.get_child_element_array(element)
        # clean the reference array
        for row in element_array:
            splitted_reference = row.split(":")
            if splitted_reference[0].strip() == elementList.reference:
                all_references.append(splitted_reference[1].strip())
    
    LOG.post_log("saving the following references to the database: {}".format(str(all_references)), logging.DEBUG)

    for reference in all_references:
        db_response = db_instance.insert_data(reference, str(hadith_book))
        if is_error(db_response):
            LOG.post_log("{}: error occured while inserting a reference: {} page element list, error: {}".format(errorPfx, reference, e), logging.ERROR)
            continue
        LOG.post_log("successfully inserted data reference: {}".format(reference), logging.DEBUG)
        time.sleep(1)
    

print("Process complete. Press any key to exit...")
input()
driver.quit()