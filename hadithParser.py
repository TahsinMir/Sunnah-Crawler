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
    
    def parse_chapter_no_and_name(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            chapter_no_element = self.driver_operation_instance.get_element(elementList.chapter_no)        
            chapter_no_element_text = self.driver_operation_instance.get_element_text(chapter_no_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting chapter no, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        

        try:
            chapter_name_element = self.driver_operation_instance.get_element(elementList.chapter_name)            
            chapter_name_element_text = self.driver_operation_instance.get_element_text(chapter_name_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting chapter name, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg
        
        return self.clean_text(chapter_no_element_text), self.clean_text(chapter_name_element_text)

    def parse_english_text(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            full_english_element = self.driver_operation_instance.get_element(elementList.english_hadith_full)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting full english element, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg


        # Hadith Narrated
        try:
            english_narrated_text_element = self.driver_operation_instance.get_child_element(full_english_element, elementList.narrated_text)
            english_narrated_text_str = self.driver_operation_instance.get_element_text(english_narrated_text_element)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while getting english narrated text, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg, errorMsg

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
        


