from colorama import init
from colorama import Fore
from colorama import Style

import logging

class Logger(object):
    def __init__(self):
        init(convert=True)

    def post_log(self, message, log_type):
        if log_type == logging.INFO:
            print(Fore.GREEN + message + Style.RESET_ALL)
        elif log_type == logging.DEBUG:
            print(Fore.CYAN + message + Style.RESET_ALL)
        elif log_type == logging.ERROR:
            print(Fore.RED + message + Style.RESET_ALL)
        return message

LOG = Logger()