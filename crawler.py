from commonVariables import sunnah_book_list
import time

class Crawler:
    def __init__(self, logger, driver, hadith_book, hadith_no):
        self.root_url = "https://sunnah.com"
        self.logger = logger
        self.driver = driver
        self.hadith_book = hadith_book
        self.hadith_no = hadith_no
    
    def visit_page(self):
        self.driver.get(self.root_url + "/" + self.hadith_book + ":" + str(self.hadith_no))
        time.sleep(10)
    
