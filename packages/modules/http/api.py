import functools
from typing import Callable, Union

import requests

from helpermodules import log


def request_value(url: str) -> float:
    if "none" == url:
        return 0
    else:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        response.encoding = 'utf-8'
        log.MainLogger().debug("Antwort auf "+str(url)+" "+str(response.text))
        return float(response.text.replace("\n", ""))


def create_request_function(domain: str, path: str) -> Callable[[], Union[int, float]]:
    if path == "none":
        return lambda: 0
    else:
        return functools.partial(request_value, domain + path)
