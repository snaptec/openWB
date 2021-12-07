from pathlib import Path
from typing import Iterable, Optional

from modules.common.store._util import get_rounding_function_by_digits, process_error

RAMDISK_PATH = Path(__file__).resolve().parents[4] / "ramdisk"


def ramdisk_write_to_files(prefix: str, values: Iterable, digits: int = None):
    for index, value in enumerate(values):
        ramdisk_write(prefix + str(index + 1), value, digits)


def ramdisk_write(file: str, value, digits: Optional[int] = None) -> None:
    try:
        rounding = get_rounding_function_by_digits(digits)
        with open(RAMDISK_PATH / file, "w") as f:
            f.write(str(rounding(value)))
    except Exception as e:
        process_error(e)
