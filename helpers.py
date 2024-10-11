import types
import sys
import logging
from typing import cast

from commonVariables import errorPfx
import elementList
import commonVariables

def get_function_name(current_frame):
    return str(cast(types.FrameType, current_frame).f_code.co_name)

def is_error(message):
    if isinstance(message, str):
        if errorPfx in message:
            return True
    
    return False

def quit_app_with_wait(logger, message):
    logger.post_log("existing app after error: {}".format(message), logging.ERROR)
    input()
    sys.exit(1)

def add_indent(number = 0):
    result = ""
    for i in range(number):
        result = result + "\t"
    return result

def parse_hadith_reference(reference):
    book = ""
    number = ""
    if reference.startswith(elementList.reference_bukhari):
        book = commonVariables.bukhari
        number = reference.replace(elementList.reference_bukhari + " ", "")
    elif reference.startswith(elementList.reference_muslim):
        book = commonVariables.muslim
        number = reference.replace(elementList.reference_muslim + " ", "")
    elif reference.startswith(elementList.reference_sunan_nasai):
        book = commonVariables.nasai
        number = reference.replace(elementList.reference_sunan_nasai + " ", "")
    elif reference.startswith(elementList.reference_sunan_dawud):
        book = commonVariables.abudawud
        number = reference.replace(elementList.reference_sunan_dawud + " ", "")
    elif reference.startswith(elementList.reference_tirmidhi):
        book = commonVariables.tirmidhi
        number = reference.replace(elementList.reference_tirmidhi + " ", "")
    elif reference.startswith(elementList.reference_sunan_majah):
        book = commonVariables.ibnmajah
        number = reference.replace(elementList.reference_sunan_majah + " ", "")
    
    return book, number