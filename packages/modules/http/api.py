import functools
import logging
from typing import Callable, Optional

from modules.common import req

log = logging.getLogger(__name__)


def request_value(url: str) -> Optional[float]:
    if "none" == url:
        return None
    else:
        response = req.get_http_session().get(url, timeout=5)
        response.encoding = 'utf-8'
        log.debug("Antwort auf "+str(url)+" "+str(response.text))
        return float(response.text.replace("\n", ""))


def create_request_function(url: str, path: str) -> Callable[[], Optional[float]]:
    if path == "none" or path is None:
        return lambda: 0
    else:
        return functools.partial(request_value, url + path)
