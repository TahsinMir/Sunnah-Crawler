# python
import inspect
import logging
from selenium.webdriver.common.by import By

# project
import helpers
from commonVariables import errorPfx


class DriverOperations:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
    
    def get_element(self, element_class):
        fn = helpers.get_function_name(inspect.currentframe())
        element = None
        try:
            element = self.driver.find_element(By.CLASS_NAME, element_class)
        except Exception as e:
            element = self.logger.post_log("{}: {}: error occured while getting element, error: {}".format(errorPfx, fn, e), logging.ERROR)
        if element is None:
            element = self.logger.post_log("{}: {}: element is none".format(errorPfx, fn), logging.ERROR)
        return element
    
    def get_child_elements(self, element, element_class):
        fn = helpers.get_function_name(inspect.currentframe())
        child_elements = None
        try:
            child_elements = element.find_element(By.CLASS_NAME, element_class)
        except Exception as e:
            child_elements = self.logger.post_log("{}: {}: error occured while getting child_elements, error: {}".format(errorPfx, fn, e), logging.ERROR)
        if child_elements is None:
            child_elements = self.logger.post_log("{}: {}: child_elements is none".format(errorPfx, fn), logging.ERROR)
        return child_elements
    
    def get_element_text(self, element):
        fn = helpers.get_function_name(inspect.currentframe())
        element_text = None
        try:
            element_text = element.text
        except Exception as e:
            element = self.logger.post_log("{}: {}: error occured while getting element_text, error: {}".format(errorPfx, fn, e), logging.ERROR)
        if element_text is None:
            element_text = self.logger.post_log("{}: {}: element text is none".format(errorPfx, fn), logging.ERROR)
        return element_text