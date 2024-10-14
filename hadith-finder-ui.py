# UI
import PySimpleGUI as sg
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
import datetime
import os.path
from colorama import Fore
from colorama import Style


def FindString(find_text, keys, values):
    found_hadiths_keys = []
    for i in range(0, len(values)):
        if find_text.lower() in values[i].lower():
            found_hadiths_keys.append(keys[i])
        # else:
        #     print("no match")
    return len(found_hadiths_keys), found_hadiths_keys

###### Copy paste begin
LOG.post_log("Starting hadith finder....", logging.INFO)


# Creating DB instance
LOG.post_log("Creating DB instance....", logging.INFO)
db_instance = databaseHadith.DatabaseHadith(LOG)
db_instance.create_database()
LOG.post_log("Successfully created DB instance..", logging.INFO)
time.sleep(3)

# Creating hadith processor
# LOG.post_log("Creating hadith processor....", logging.INFO)
# hadith_processor = HadithProcessor()
# LOG.post_log("Successfully created hadith processor..", logging.INFO)
# time.sleep(3)
###### Copy paste end

print("time before reading data:")
print(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
hadith_keys, hadith_values  = db_instance.get_all_data()
print(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('This is the Hadith Finder', text_color='lightblue')],
			[sg.Text('Search string', text_color='green'), sg.InputText()],
            [sg.Button('Search'), sg.Button('Quit')] ]

# Create the Window
window = sg.Window('Hadith Finder', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # temp = values[1]
    # forbidden = values[2]
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        break
    if event == 'Search':
        searchStr = values[0]
        result_number, result_keys = FindString(searchStr, hadith_keys, hadith_values)
        sg.Popup(str(result_number) + str(result_keys))
    	#result = CheckRegex(confirmed, temp, forbidden)
    	#if result == "looks good":
    	#	wordList = GetFinalWordList(confirmed, temp, forbidden)
    	#	if len(wordList) > 50:
    	#		wordList = wordList[0:50]
    	#	sg.Popup(str(wordList))
    	#else:
    	#	sg.Popup(result)

window.close()