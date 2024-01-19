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

# Creating DB instance
LOG.post_log("Creating DB instance....", logging.INFO)
db_instance = databaseHadith.DatabaseHadith(LOG)
db_instance.create_database()
LOG.post_log("Successfully created DB instance..", logging.INFO)
time.sleep(3)

# get all data
keys, values  = db_instance.get_all_data()


# filtered keys
filtered_keys = []
for key in keys:
    splitted = key.split(" ")
    for split in splitted:
        split = split.replace(",", '').strip()

        # check integers only
    try:
        split_int = int(split)
        filtered_keys.append(split_int)
    except ValueError:
        print("exception for: ")
        print(split)
        continue


# for key in filtered_keys:
#    print(key)
# for i in range (1, 7564):
#     if i not in filtered_keys:
#         print(i)