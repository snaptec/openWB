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
