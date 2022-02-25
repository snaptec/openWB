import json
import logging
from json import JSONDecodeError
from typing import Callable

import requests
from requests import HTTPError

from modules.common.req import get_http_session
from modules.common.store import RAMDISK_PATH

COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
log = logging.getLogger("Powerwall")


class PowerwallHttpClient:
    def __init__(self, host: str, session: requests.Session, cookies):
        self.__base_url = "https://" + host
        self.__cookies = cookies
        self.__session = session

    def get_json(self, relative_url: str):
        url = self.__base_url + relative_url
        return self.__session.get(url, cookies=self.__cookies, verify=False, timeout=5).json()


UpdateFunction = Callable[[PowerwallHttpClient], None]


def _authenticate(session: requests.Session, url: str, email: str, password: str):
    """
    email is not yet required for login (2022/01), but we simulate the whole login page
    """
    response = session.post(
        "https://" + url + "/api/login/Basic",
        json={"username": "customer", "email": email, "password": password},
        verify=False,
        timeout=5
    )
    log.debug("Authentication endpoint send cookies %s", str(response.cookies))
    return {"AuthCookie": response.cookies["AuthCookie"], "UserRecord": response.cookies["UserRecord"]}


def _authenticate_and_update(session: requests.Session,
                             address: str,
                             email: str,
                             password: str,
                             update_function: UpdateFunction):
    cookie = _authenticate(session, address, email, password)
    COOKIE_FILE.write_text(json.dumps(cookie))
    update_function(PowerwallHttpClient(address, session, cookie))


def powerwall_update(address: str, email: str, password: str, update_function: UpdateFunction):
    log.debug("Beginning update")
    cookies = None
    try:
        cookies = json.loads(COOKIE_FILE.read_text())
    except FileNotFoundError:
        log.debug("Cookie-File <%s> does not exist. It will be created.", COOKIE_FILE)
    except JSONDecodeError as e:
        log.warning("Could not parse Cookie-File <%s>. It will be re-created.", COOKIE_FILE, exc_info=e)

    session = get_http_session()
    if cookies is None:
        _authenticate_and_update(session, address, email, password, update_function)
        return
    try:
        update_function(PowerwallHttpClient(address, session, cookies))
        return
    except HTTPError as e:
        if e.response.status_code != 401 and e.response.status_code != 403:
            raise e
        log.warning("Login to powerwall with existing cookie failed. Will retry with new cookie...")
    _authenticate_and_update(session, address, email, password, update_function)
    log.debug("Update completed successfully")
