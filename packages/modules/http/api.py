import functools
from typing import Callable, Union

from helpermodules import log
from modules.common import req


def request_value(url: str) -> float:
    if "none" == url:
        return 0
    else:
        response = req.get_text(url, timeout=5)
        log.MainLogger().debug("Antwort auf "+str(url)+" "+str(response))
        return float(response.replace("\n", ""))


def create_request_function(domain: str, path: str) -> Callable[[], Union[int, float]]:
    if path == "none":
        return lambda: 0
    else:
        return functools.partial(request_value, domain + path)
