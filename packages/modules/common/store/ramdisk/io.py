from pathlib import Path
from typing import Iterable, Optional, TypeVar, Callable

from modules.common.store._util import get_rounding_function_by_digits, process_error

RAMDISK_PATH = Path(__file__).resolve().parents[5] / "ramdisk"

T = TypeVar('T')


class RamdiskReadError(Exception):
    def __init__(self, file: str, content: str, message: str):
        super().__init__("Error reading ramdisk file <{}>, content=<{}>: {}".format(file, content, message))


def ramdisk_write_to_files(prefix: str, values: Iterable, digits: int = None):
    for index, value in enumerate(values):
        ramdisk_write(prefix + str(index + 1), value, digits)


def ramdisk_write(file: str, value, digits: Optional[int] = None) -> None:
    try:
        (RAMDISK_PATH / file).write_text(str(get_rounding_function_by_digits(digits)(value)))
    except Exception as e:
        process_error(e)


def ramdisk_read(file: str) -> str:
    # Using `strip`, because oftentimes values are written from bash like `echo value > file` which adds a newline at
    # the end of file
    return (RAMDISK_PATH / file).read_text().strip()


def ramdisk_read_mapping(file: str, mapper: Callable[[str], T], error_message: str) -> T:
    file_content = ramdisk_read(file)
    try:
        return mapper(file_content)
    except ValueError as e:
        raise RamdiskReadError(file, file_content, error_message) from e


def ramdisk_read_int(file: str) -> int:
    return ramdisk_read_mapping(file, int, "expected int")


def ramdisk_read_float(file: str) -> float:
    return ramdisk_read_mapping(file, float, "expected float")
