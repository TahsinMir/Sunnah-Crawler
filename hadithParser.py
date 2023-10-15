# project
import elementList
import helpers

# python
import logging

class HadithParser:
    def __init__(self, driver_operation_instance, logger):
        self.driver_operation_instance = driver_operation_instance
        self.logger = logger
    
    def parse_chapter_no_and_name(self):
        chapter_no_element = self.driver_operation_instance.get_element(elementList.chapter_no)
        if helpers.is_error(chapter_no_element):
            helpers.quit_app_with_wait(self.logger, chapter_no_element)
        
        chapter_no_element_text = self.driver_operation_instance.get_element_text(chapter_no_element)
        if helpers.is_error(chapter_no_element_text):
            helpers.quit_app_with_wait(self.logger, chapter_no_element_text)
        

        chapter_name_element = self.driver_operation_instance.get_element(elementList.chapter_name)
        if helpers.is_error(chapter_name_element):
            helpers.quit_app_with_wait(self.logger, chapter_name_element)
        
        chapter_name_element_text = self.driver_operation_instance.get_element_text(chapter_name_element)
        if helpers.is_error(chapter_name_element_text):
            helpers.quit_app_with_wait(self.logger, chapter_name_element_text)
        
        return chapter_no_element_text, chapter_name_element_text

    def parse_english_text(self):
        full_english_element = self.driver_operation_instance.get_element(elementList.english_hadith_full)
        if helpers.is_error(full_english_element):
            helpers.quit_app_with_wait(self.logger, full_english_element)


        # Hadith Narrated
        english_hadith_narrated = self.driver_operation_instance.get_child_element(full_english_element, elementList.hadith_narrated)
        if helpers.is_error(english_hadith_narrated):
            helpers.quit_app_with_wait(self.logger, english_hadith_narrated)


        english_hadith_narrated_text = self.driver_operation_instance.get_element_text(english_hadith_narrated)
        if helpers.is_error(english_hadith_narrated_text):
            helpers.quit_app_with_wait(self.logger, english_hadith_narrated_text)

        # Hadith details
        english_hadith_details = self.driver_operation_instance.get_child_element(full_english_element, elementList.hadith_text_details)
        if helpers.is_error(english_hadith_details):
            helpers.quit_app_with_wait(self.logger, english_hadith_details)


        english_hadith_details_text = self.driver_operation_instance.get_element_text(english_hadith_details)
        if helpers.is_error(english_hadith_details_text):
            helpers.quit_app_with_wait(self.logger, english_hadith_details_text)
        
        
        return english_hadith_narrated_text, english_hadith_details_text


    def parse_reference(self):
        full_reference_element = self.driver_operation_instance.get_element(elementList.hadith_reference)
        if helpers.is_error(full_reference_element):
            helpers.quit_app_with_wait(self.logger, full_reference_element)

        reference_array = self.driver_operation_instance.get_child_element_array(full_reference_element)
        
        # clean the reference array
        referenceDict = {}
        for row in reference_array:
            splitted_reference = row.split(":")
            if splitted_reference[0].strip() in elementList.type_of_reference:
                referenceDict[splitted_reference[0].strip()] = splitted_reference[1].strip()


        return referenceDict
        


