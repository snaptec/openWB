import functools
import logging
from typing import Callable, Optional

from modules.common import req

log = logging.getLogger(__name__)


def _request_value(url: str) -> float:
    response_text = req.get_http_session().get(url, timeout=5).text
    log.debug("Antwort auf %s: %s", url, response_text)
    return float(response_text.replace("\n", ""))


def create_request_function(url: str, path: Optional[str]) -> Callable[[], float]:
    if path == "none" or path is None:
        return lambda: None
    else:
        return functools.partial(_request_value, url + path)
