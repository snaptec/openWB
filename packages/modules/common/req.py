
import requests

from helpermodules import log


def get_json(url, params=None, **kwargs) -> dict:
    return __get(url, params, **kwargs).json()


def get_text(url, params=None, **kwargs) -> str:
    return __get(url, params, **kwargs).text


def __get(url, params, **kwargs) -> requests.Response:
    response = requests.get(url, params, **kwargs)
    response.raise_for_status()
    response.encoding = 'utf-8'
    log.MainLogger().debug("Get-Response " + url + ": " + response.text)
    return response
