import types
import sys
import logging
from typing import cast

from commonVariables import errorPfx

def get_function_name(current_frame):
    return str(cast(types.FrameType, current_frame).f_code.co_name)

def is_error(message):
    if isinstance(message, str):
        if errorPfx in message:
            return True
    
    return False

def quit_app_with_wait(logger, message):
    logger.post_log("existing app after error: {}".format(message), logging.ERROR)
    sys.exit(1)