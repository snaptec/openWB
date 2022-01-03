from typing import Union

from modules.common import req

_SOC_PROPERTY = "soc_display"


def fetch_soc(akey: str, token: str) -> Union[int, float]:
    response = req.get_http_session().get("https://app.evnotify.de/soc", params={"akey": akey, "token": token})
    try:
        soc_display = response.json()[_SOC_PROPERTY]
        if not isinstance(soc_display, (int, float)):
            raise Exception("Number expected, got <{}>, type={}".format(soc_display, type(soc_display)))
        return soc_display
    except Exception as e:
        raise Exception(
            "Expected object with numeric property <{}>. Got: <{}>".format(_SOC_PROPERTY, response.text)
        ) from e
