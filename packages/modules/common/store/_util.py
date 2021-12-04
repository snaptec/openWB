from typing import Callable, Union

from modules.common.fault_state import FaultState


def get_rounding_function_by_digits(digits: Union[int, None]) -> Callable:
    if digits is None:
        return lambda value: value
    elif digits == 0:
        return int
    else:
        return lambda value: round(value, digits)


def process_error(e):
    raise FaultState.error(__name__+" "+str(type(e))+" "+str(e)) from e
