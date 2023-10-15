import elementList
import helpers


class HadithParser:
    def __init__(self, driver_operation_instance, logger):
        self.driver_operation_instance = driver_operation_instance
        self.logger = logger
    
    def parse_english_text(self):
        full_english_element = self.driver_operation_instance.get_element(elementList.english_hadith_full)
        if helpers.is_error(full_english_element):
            helpers.quit_app_with_wait(self.logger, full_english_element)


        # Hadith Narrated
        english_hadith_narrated = self.driver_operation_instance.get_child_elements(full_english_element, elementList.hadith_narrated)
        if helpers.is_error(english_hadith_narrated):
            helpers.quit_app_with_wait(self.logger, english_hadith_narrated)


        english_hadith_narrated_text = self.driver_operation_instance.get_element_text(english_hadith_narrated)
        if helpers.is_error(english_hadith_narrated_text):
            helpers.quit_app_with_wait(self.logger, english_hadith_narrated_text)

        # Hadith details
        english_hadith_details = self.driver_operation_instance.get_child_elements(full_english_element, elementList.hadith_text_details)
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

        full_reference_element_text = self.driver_operation_instance.get_element_text(full_reference_element)
        if helpers.is_error(full_reference_element_text):
            helpers.quit_app_with_wait(self.logger, full_reference_element_text)

        print(type(full_reference_element_text))
        return full_reference_element_text
        


