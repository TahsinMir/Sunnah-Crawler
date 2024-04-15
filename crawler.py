from commonVariables import sunnah_book_list, errorPfx, success
import helpers
import inspect
import elementList

import time
import logging

class Crawler:
    def __init__(self, logger, driver, driver_operation_instance):
        self.root_url = "https://sunnah.com"
        self.logger = logger
        self.driver = driver
        self.driver_operation_instance = driver_operation_instance
    
    def go_to_hadith_book(self, hadith_book_name, hadith_book_no):
        fn = helpers.get_function_name(inspect.currentframe())
        url = self.root_url + "/" + hadith_book_name + "/" + str(hadith_book_no)
        if helpers.is_error(url):
            errorMsg = self.logger.post_log("{}: {}: error occured while generating url: {}".format(errorPfx, fn, url), logging.ERROR)
        
        try:
            self.driver.get(url)
            self.logger.post_log("{}: visited page: {}".format(fn, url), logging.INFO)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while visiting page: {}, error: {}".format(errorPfx, fn, url, e), logging.ERROR)
            return errorMsg
        
        time.sleep(3)
        return success

    def visit_to_hadith_page(self, hadith_book, hadith_no):
        fn = helpers.get_function_name(inspect.currentframe())
        url = self.generate_url(hadith_book, hadith_no)
        if helpers.is_error(url):
            errorMsg = self.logger.post_log("{}: {}: error occured while generating url: {}".format(errorPfx, fn, url), logging.ERROR)
        
        try:
            self.driver.get(url)
            self.logger.post_log("{}: visited page: {}".format(fn, url), logging.INFO)
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while visiting page: {}, error: {}".format(errorPfx, fn, url, e), logging.ERROR)
            return errorMsg
        
        time.sleep(3)
        return success

    def go_to_next_page(self):
        fn = helpers.get_function_name(inspect.currentframe())
        try:
            next_page_button = self.driver_operation_instance.get_element(elementList.next_page)
            if helpers.is_error(next_page_button):
                helpers.quit_app_with_wait(self.logger, next_page_button)
        
            next_page_button.click()
        except Exception as e:
            errorMsg = self.logger.post_log("{}: {}: error occured while moving to next page, error: {}".format(errorPfx, fn, e), logging.ERROR)
            return errorMsg
        
        time.sleep(3)
        return success

        
    
    def check_hadith_book(self, hadith_book):
        if hadith_book not in sunnah_book_list:
            return False
        return True
    
    def generate_url(self, hadith_book, hadith_no):
        fn = helpers.get_function_name(inspect.currentframe())
        if not self.check_hadith_book(hadith_book):
            return self.logger.post_log("{}: {}: invalid hadith_book: {}".format(errorPfx, fn, hadith_book), logging.ERROR)
        # commenting out because hadith links can contain non integers
        #if not isinstance(hadith_no, int):
        #    return self.logger.post_log("{}: {}: invalid hadith_no: {}".format(errorPfx, fn, hadith_no), logging.ERROR)
        
        return self.root_url + "/" + hadith_book + ":" + str(hadith_no)




    
