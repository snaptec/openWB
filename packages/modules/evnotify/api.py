from typing import Union

import requests

_SOC_PROPERTY = "soc_display"


def fetch_soc(akey: str, token: str) -> Union[int, float]:
    response = requests.get("https://app.evnotify.de/soc", params={"akey": akey, "token": token})
    response.raise_for_status()
    try:
        soc_display = response.json()[_SOC_PROPERTY]
        if not isinstance(soc_display, (int, float)):
            raise Exception("Number expected, got <{}>, type={}".format(soc_display, type(soc_display)))
        return soc_display
    except Exception as e:
        raise Exception(
            "Expected object with numeric property <{}>. Got: <{}>".format(_SOC_PROPERTY, response.text)
        ) from e
