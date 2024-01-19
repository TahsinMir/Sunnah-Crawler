# project
from log import LOG
from helpers import is_error, quit_app_with_wait
import databaseHadith
import commonVariables
import hadithParser
from hadith import Hadith, ChapterInfo, Text, EnglishText, ArabicText, Reference, HadithProcessor

# python
import logging
import time
import json
import os
from unidecode import unidecode
from fpdf import FPDF
import pandas as pd
import arabic_reshaper # pip install arabic_reshaper


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


# Take in input creating file
# LOG.post_log("Enter hadith book....", logging.INFO)
# hadith_book = input()
# if hadith_book not in commonVariables.sunnah_book_list:
#     quit_app_with_wait(LOG, "Hadith book name '{}' is invalid".format(hadith_book))
# LOG.post_log("Hadith book name '{}' is valid".format(hadith_book), logging.INFO)
# time.sleep(3)




# Printing wanring sign to proceed
LOG.post_log("Proceeding with file creation in ten seconds...", logging.DEBUG)
#time.sleep(10)


keys, values  = db_instance.get_all_data()

# pdf object
pdf = FPDF()
# Download NotoSansArabic-Regular.ttf from Google noto fonts
# pdf.add_font("NotoSansArabic", style="", fname=os.getcwd() + "\\" + "fonts\\NotoSansArabic-Regular.ttf", uni=True)
# pdf.add_font("NotoSansArabicBlack", style="", fname=os.getcwd() + "\\" + "fonts\\NotoSansArabic-Black.ttf", uni=True)
# pdf.add_font("NotoSansArabicCondensed", style="", fname=os.getcwd() + "\\" + "fonts\\NotoSansArabic_Condensed-Regular.ttf", uni=True)
# pdf.add_font('DejaVu', style="", fname=os.getcwd() + "\\" + "fonts\\DejaVuSansCondensed.ttf", uni=True)
# pdf.add_font('DejaVuSans', style="", fname=os.getcwd() + "\\" + "fonts\\DejaVuSans.ttf", uni=True)
# pdf.add_font('DejaVuSerif', style="", fname=os.getcwd() + "\\" + "fonts\\DejaVuSerif.ttf", uni=True)
# pdf.add_font('DejaVuSansMono', style="", fname=os.getcwd() + "\\" + "fonts\\DejaVuSansMono.ttf", uni=True)


# Create hadith object
for hadith_json in values:
    hadith_obj = hadith_processor.json_to_hadith(hadith_json)

    # new page
    pdf.add_page()

    # book
    pdf.set_font('Arial', 'B', 15)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(w = 0, h = 10, txt="Book No: " + hadith_obj.book_info.book_no + ", Book Name: " + hadith_obj.book_info.book_name, border = 0, ln = 1, align = 'L', fill = False)


    # blank space
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(w = 0, h = 5, txt="ABCDEF", border = 0, ln = 1, align = 'L', fill = False)

    # chapter
    pdf.set_font('Arial', 'B', 15)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(w = 0, h = 10, txt="Chapter No: " + hadith_obj.chapter_info.chapter_no + ", Chapter Name: " + hadith_obj.chapter_info.chapter_name, border = 0, ln = 1, align = 'L', fill = False)


    # blank space
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(w = 0, h = 5, txt="ABCDEF", border = 0, ln = 1, align = 'L', fill = False)

    # hadith title
    book = hadith_obj.reference.reference.rsplit(" ", 1)[0]
    number = hadith_obj.reference.reference.rsplit(" ", 1)[1]
    pdf.set_font('Arial', 'B', 15)
    pdf.set_text_color(r=32, g=107, b=88)
    pdf.cell(w = 0, h = 10, txt="Hadith Book: " + book + ", Hadith No: " + number, border = 0, ln = 1, align = 'L', fill = False)

    # english text
    # narrated
    pdf.set_text_color(r=93,g=128,b=128)
    pdf.set_font('Arial', 'B', 11)
    pdf.multi_cell(0, 5, unidecode(hadith_obj.text.english_text.narrated_text), border=0, align='L')

    # blank space
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(w = 0, h = 4, txt="ABCDEF", border = 0, ln = 1, align = 'L', fill = False)

    # description
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font('Arial', '', 9)
    pdf.multi_cell(0, 5, unidecode(hadith_obj.text.english_text.details_text), border=0, align='L')


    # blank space
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(w = 0, h = 4, txt="ABCDEF", border = 0, ln = 1, align = 'L', fill = False)


    # reference header
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(w = 0, h = 5, txt="Reference", border = 0, ln = 1, align = 'L', fill = False)

    


    # arabic text
    # does not work well
    # pdf.set_font('DejaVuSans', '', 10)
    # arabic_string = arabic_reshaper.reshape(hadith_obj.text.arabic_text.full_arabic_text)
    # arabic_string = arabic_string[::-1]
    # w = pdf.get_string_width(arabic_string) + 6
    # pdf.multi_cell(w=0, h=5, txt=arabic_string, border=1, align='R', fill=False)
    # pdf.multi_cell(0, 5, txt=arabic_string, border=1, align='L', fill=False)
    # pdf.cell(0, 5, txt=hadith_obj.text.arabic_text.full_arabic_text, border=1, ln=2, align='L', fill=False)

    # reference
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.multi_cell(w=0, h=4, txt=hadith_obj.reference.reference + "\n" + hadith_obj.reference.in_book_reference + "\n" + hadith_obj.reference.uscmsa_web_reference, border=0, align='L')


    # blank space
    pdf.set_font('Arial', '', 8)
    pdf.set_text_color(r=255, g=255, b=255)
    pdf.cell(w = 0, h = 4, txt="ABCDEF", border = 0, ln = 1, align = 'L', fill = False)

    # url header
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(w = 0, h = 5, txt="Link", border = 0, ln = 1, align = 'L', fill = False)


    # url
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.cell(w=0, h=4, txt=hadith_obj.link.url, border=0, ln = 1, align='L', link =hadith_obj.link.url)


pdf.output('tuto1.pdf', 'F')
