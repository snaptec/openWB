import functools
import logging
from typing import Callable, Optional, Iterable, List

from modules.common import req

log = logging.getLogger(__name__)


def _request_value(url: str) -> float:
    response_text = req.get_http_session().get(url, timeout=5).text
    log.debug("Antwort auf %s: %s", url, response_text)
    return float(response_text.replace("\n", ""))


def create_request_function(url: str, path: Optional[str]) -> Callable[[], Optional[float]]:
    if path is None:
        return lambda: None
    else:
        return functools.partial(_request_value, url + path)


def create_request_function_array(url: str, paths: Iterable[Optional[str]]) -> Callable[[], Optional[List[float]]]:
    functions = []  # type: List[Callable[[], float]]
    for path in paths:
        if path is not None:
            functions.append(functools.partial(_request_value, url + path))
        elif functions:
            raise Exception("Expected all or no paths to be None, got: <%s>" % paths)
    if functions:
        return lambda: [function() for function in functions]
    return lambda: None
