import threading
from typing import Callable, TypeVar

T = TypeVar("T")


def skip_while_unchanged(source: Callable, initial=None):
    """Before each call check if value given by `source` has changed. If it has not, ignore the call"""
    def wrap(function: T) -> T:
        previous = [initial]
        lock = threading.Lock()

        def wrapper(*args, **kwargs):
            with lock:
                next = source()
                if previous[0] != next:
                    function(*args, **kwargs)
                    previous[0] = next

        return wrapper

    return wrap
