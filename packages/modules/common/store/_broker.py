from typing import Union

from helpermodules.pub import Pub
from modules.common.store._util import get_rounding_function_by_digits, process_error


def pub_to_broker(topic: str, value, digits: Union[int, None] = None) -> None:
    rounding = get_rounding_function_by_digits(digits)
    try:
        if isinstance(value, list):
            Pub().pub(topic, [rounding(v) for v in value])
        else:
            Pub().pub(topic, rounding(value))
    except Exception as e:
        process_error(e)
