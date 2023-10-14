import types
from typing import cast

def get_function_name(current_frame):
    return str(cast(types.FrameType, current_frame).f_code.co_name)