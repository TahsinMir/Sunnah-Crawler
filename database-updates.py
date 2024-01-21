# project
import browserDriver
import crawler
import driverOperations
import hadithParser
import elementList
import databaseHadith
import commonVariables
import timeFunctions
from log import LOG
from helpers import is_error, quit_app_with_wait
from hadith import Hadith, BookInfo, ChapterInfo, Text, Link, EnglishText, ArabicText, Reference, HadithProcessor

# python
import json
import time
import logging
from colorama import Fore
from colorama import Style

# Hadith
# Creating DB instance
LOG.post_log("Creating DB instance....", logging.INFO)
db_instance = databaseHadith.DatabaseHadith(LOG)
db_instance.create_database()
LOG.post_log("Successfully created DB instance..", logging.INFO)
time.sleep(3)


# 1
# Update Last Updated -- current time
# query = "ALTER TABLE Hadiths ADD COLUMN LAST_UPDATED TEXT DEFAULT NULL;"
# response = db_instance.run_alter_query(query)
# LOG.post_log(str(response), logging.DEBUG)

# current_time = timeFunctions.get_current_time()
# print(current_time)
# query = 'UPDATE Hadiths SET LAST_UPDATED = "{}"'.format(current_time)
# response = db_instance.run_update_query(query)
# LOG.post_log(str(response), logging.DEBUG)


# 2
# Update Sahih -- bool
# query = 'ALTER TABLE Hadiths ADD COLUMN Grade TEXT DEFAULT "Grade: Sahih (Darussalam)";'
# response = db_instance.run_alter_query(query)
# LOG.post_log(str(response), logging.DEBUG)

# Hadith Links
