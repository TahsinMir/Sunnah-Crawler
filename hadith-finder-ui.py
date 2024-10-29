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


def FindString(find_text, keys, values, allowed_books):
    found_hadiths_keys = []
    for i in range(0, len(values)):
        if find_text.lower() in values[i].lower():
            if IsBookMatch(keys[i], allowed_books):
                found_hadiths_keys.append(keys[i])
        # else:
        #     print("no match")
    return len(found_hadiths_keys), found_hadiths_keys


def IsBookMatch(hadith_key, allowed_books):
    hadith_key_type = None
    if elementList.reference_bukhari in hadith_key:
        hadith_key_type = commonVariables.bukhari
    elif elementList.reference_muslim in hadith_key:
        hadith_key_type = commonVariables.muslim
    elif elementList.reference_sunan_nasai in hadith_key:
        hadith_key_type = commonVariables.nasai
    elif elementList.reference_sunan_dawud in hadith_key:
        hadith_key_type = commonVariables.abudawud
    elif elementList.reference_tirmidhi in hadith_key:
        hadith_key_type = commonVariables.tirmidhi
    elif elementList.reference_sunan_majah in hadith_key:
        hadith_key_type = commonVariables.ibnmajah
    
    if hadith_key_type is None:
        return False
    return allowed_books[hadith_key_type]

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
			[sg.Text('Search String', text_color='green'), sg.InputText(key=commonVariables.searchStr)],
            [sg.Text('Hadith Book', text_color='green'), sg.Checkbox('Bukhari', key=commonVariables.bukhari), sg.Checkbox('Muslim', key=commonVariables.muslim), sg.Checkbox('Nasai', key=commonVariables.nasai), sg.Checkbox('Abudawud', key=commonVariables.abudawud), sg.Checkbox('Tirmidhi', key=commonVariables.tirmidhi), sg.Checkbox('Ibnmajah', key=commonVariables.ibnmajah)],
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
        print("just printing all values to understand")
        print(values)
        searchStr = values[commonVariables.searchStr]
        allowed_books = {
            commonVariables.bukhari: values[commonVariables.bukhari],
            commonVariables.muslim: values[commonVariables.muslim],
            commonVariables.nasai: values[commonVariables.nasai],
            commonVariables.abudawud: values[commonVariables.abudawud],
            commonVariables.tirmidhi: values[commonVariables.tirmidhi],
            commonVariables.ibnmajah: values[commonVariables.ibnmajah]
        }
        all_false = all(value is False for value in allowed_books.values())
        if all_false:
            allowed_books = {
            commonVariables.bukhari: True,
            commonVariables.muslim: True,
            commonVariables.nasai: True,
            commonVariables.abudawud: True,
            commonVariables.tirmidhi: True,
            commonVariables.ibnmajah: True
        }
        result_number, result_keys = FindString(searchStr, hadith_keys, hadith_values, allowed_books)
        if len(result_keys) > 10:
            result_keys = result_keys[:10]
        sg.Popup("Total match count: " + str(result_number) + ", Sample: " + str(result_keys))
    	#result = CheckRegex(confirmed, temp, forbidden)
    	#if result == "looks good":
    	#	wordList = GetFinalWordList(confirmed, temp, forbidden)
    	#	if len(wordList) > 50:
    	#		wordList = wordList[0:50]
    	#	sg.Popup(str(wordList))
    	#else:
    	#	sg.Popup(result)

window.close()