from typing import Iterable, Union

from modules.common.store._util import get_rounding_function_by_digits, process_error


def write_array_to_files(prefix: str, values: Iterable, digits: int = None):
    for index, value in enumerate(values):
        write_to_file(prefix + str(index + 1), value, digits)


def write_to_file(file: str, value, digits: Union[int, None] = None) -> None:
    try:
        rounding = get_rounding_function_by_digits(digits)
        with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
            f.write(str(rounding(value)))
        return value
    except Exception as e:
        process_error(e)
