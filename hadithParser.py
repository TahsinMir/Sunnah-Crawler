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
        english_narrated_text_element = self.driver_operation_instance.get_child_element(full_english_element, elementList.narrated_text)
        if helpers.is_error(english_narrated_text_element):
            helpers.quit_app_with_wait(self.logger, english_narrated_text_element)


        english_narrated_text_str = self.driver_operation_instance.get_element_text(english_narrated_text_element)
        if helpers.is_error(english_narrated_text_str):
            helpers.quit_app_with_wait(self.logger, english_narrated_text_str)

        # Hadith details
        english_details_text_element = self.driver_operation_instance.get_child_element(full_english_element, elementList.details_text)
        if helpers.is_error(english_details_text_element):
            helpers.quit_app_with_wait(self.logger, english_details_text_element)


        english_details_text_str = self.driver_operation_instance.get_element_text(english_details_text_element)
        if helpers.is_error(english_details_text_str):
            helpers.quit_app_with_wait(self.logger, english_details_text_str)
        
        
        return english_narrated_text_str, english_details_text_str


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
    
    def parse_arabic_text(self):
        full_arabic_text_element = self.driver_operation_instance.get_element(elementList.full_arabic_text)
        if helpers.is_error(full_arabic_text_element):
            helpers.quit_app_with_wait(self.logger, full_arabic_text_element)
        
        full_arabic_text_element_str = self.driver_operation_instance.get_element_text(full_arabic_text_element)
        if helpers.is_error(full_arabic_text_element_str):
            helpers.quit_app_with_wait(self.logger, full_arabic_text_element_str)
        
        
        return full_arabic_text_element_str
        


