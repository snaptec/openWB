import functools
import logging
from typing import Callable, Optional, Iterable, List, TypeVar

from requests import Session

log = logging.getLogger(__name__)
T = TypeVar('T')
RequestFunction = Callable[[Session], T]


def _request_value(url: str, session: Session) -> float:
    return float(session.get(url, timeout=5).text.replace("\n", ""))


def create_request_function(url: str, path: Optional[str]) -> RequestFunction[Optional[float]]:
    if path is None:
        return lambda _: None
    else:
        return functools.partial(_request_value, url + path)


def create_request_function_array(url: str, paths: Iterable[Optional[str]]) -> RequestFunction[Optional[List[float]]]:
    functions = []  # type: List[RequestFunction[float]]
    for path in paths:
        if path is not None:
            functions.append(functools.partial(_request_value, url + path))
        elif functions:
            raise Exception("Expected all or no paths to be None, got: <%s>" % paths)
    if functions:
        return lambda session: [function(session) for function in functions]
    return lambda _: None
