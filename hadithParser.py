# project
import elementList
import helpers
from commonVariables import errorPfx, success

# python
import logging
import inspect

class HadithParser:
    def __init__(self, driver_operation_instance, logger):
        self.driver_operation_instance = driver_operation_instance
        self.logger = logger
    
    def parse_book_no_and_name(self):
        fn = helpers.get_function_name(inspect.currentframe())
        book_no_str = ""
        book_name_str = ""

        try:
            book_no_element = self.driver_operation_instance.get_element(elementList.book_no)
            book_no_element_text = self.driver_operation_instance.get_element_text(book_no_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting book no, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        if book_no_element_text is not None and not helpers.is_error(book_no_element_text):
            book_no_str = book_no_element_text

        try:
            book_name_element = self.driver_operation_instance.get_element(elementList.book_name)
            book_name_element_text = self.driver_operation_instance.get_element_text(book_name_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting book name, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        if book_name_element_text is not None and not helpers.is_error(book_name_element_text):
            book_name_str = book_name_element_text

        return self.clean_text(book_no_str), self.clean_text(book_name_str)

    def parse_chapter_no_and_name(self):
        fn = helpers.get_function_name(inspect.currentframe())
        chapter_no_str = ""
        chapter_name_str = ""

        try:
            chapter_no_element = self.driver_operation_instance.get_element(elementList.chapter_no)        
            chapter_no_element_text = self.driver_operation_instance.get_element_text(chapter_no_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting chapter no, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        if chapter_no_element_text is not None and not helpers.is_error(chapter_no_element_text):
            chapter_no_str = chapter_no_element_text

        try:
            chapter_name_element = self.driver_operation_instance.get_element(elementList.chapter_name)            
            chapter_name_element_text = self.driver_operation_instance.get_element_text(chapter_name_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting chapter name, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        if chapter_name_element_text is not None and not helpers.is_error(chapter_name_element_text):
            chapter_name_str = chapter_name_element_text
        
        return self.clean_text(chapter_no_str), self.clean_text(chapter_name_str)

    def parse_english_text(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            full_english_element = self.driver_operation_instance.get_element(elementList.english_hadith_full)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting full english element, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg

        # Hadith Narrated
        errorMsg = ""
        english_narrated_text_str = ""
        try:
            english_narrated_text_element = self.driver_operation_instance.get_child_element(full_english_element, elementList.narrated_text)
            english_narrated_text_str = self.driver_operation_instance.get_element_text(english_narrated_text_element)
        except Exception as e:
            # Narrated text is not present
            errorMsg = self.logger.post_log("{}: {}: error occured while getting english narrated text, error: {}".format(errorPfx, fn, e), logging.ERROR)

        # if narrated text is not found, then skip to the rest
        if helpers.is_error(errorMsg) or helpers.is_error(english_narrated_text_str):
            english_narrated_text_str = ""

        # Hadith details
        try:
            english_details_text_element = self.driver_operation_instance.get_child_element(full_english_element, elementList.details_text)
            english_details_text_str = self.driver_operation_instance.get_element_text(english_details_text_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting hadith details, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        
        
        return self.clean_text(english_narrated_text_str), self.clean_text(english_details_text_str)


    def parse_reference(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            full_reference_element = self.driver_operation_instance.get_element(elementList.hadith_reference)
            reference_array = self.driver_operation_instance.get_child_element_array(full_reference_element)
        
            # clean the reference array
            referenceDict = {}
            for row in reference_array:
                splitted_reference = row.split(":")
                if splitted_reference[0].strip() in elementList.type_of_reference:
                    referenceDict[splitted_reference[0].strip()] = splitted_reference[1].strip()
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting reference, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg

        # fill out absent reference types with empty
        for reference_type in elementList.type_of_reference:
            if reference_type not in referenceDict:
                referenceDict[reference_type] = ""

        return referenceDict
    
    def parse_arabic_text(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            full_arabic_text_element = self.driver_operation_instance.get_element(elementList.full_arabic_text)        
            full_arabic_text_element_str = self.driver_operation_instance.get_element_text(full_arabic_text_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting full arabic text, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg
        
        return self.clean_text(full_arabic_text_element_str)
    
    def clean_text(self, text):
        return text.strip()
        


