from commonVariables import sunnah_book_list, errorPfx
import helpers
import inspect

import time
import logging

class Crawler:
    def __init__(self, logger, driver):
        self.root_url = "https://sunnah.com"
        self.logger = logger
        self.driver = driver
    
    def visit_page(self, hadith_book, hadith_no):
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

        
    
    def check_hadith_book(self, hadith_book):
        if hadith_book not in sunnah_book_list:
            return False
        return True
    
    def generate_url(self, hadith_book, hadith_no):
        fn = helpers.get_function_name(inspect.currentframe())
        if not self.check_hadith_book(hadith_book):
            return self.logger.post_log("{}: {}: invalid hadith_book: {}".format(errorPfx, fn, hadith_book), logging.ERROR)
        if not isinstance(hadith_no, int):
            return self.logger.post_log("{}: {}: invalid hadith_no: {}".format(errorPfx, fn, hadith_no), logging.ERROR)
        
        return self.root_url + "/" + hadith_book + ":" + str(hadith_no)




    
