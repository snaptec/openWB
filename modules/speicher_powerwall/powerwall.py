#!/usr/bin/env python3

import json
import logging
from json import JSONDecodeError

import requests
from requests import HTTPError

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import BatState
from modules.common.store import get_bat_value_store, RAMDISK_PATH

COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
log = logging.getLogger("Powerwall")


def authenticate(url: str, password: str):
    response = requests.post(
        "https://" + url + "/api/login/Basic",
        json={"username": "", "password": password, "force_sm_off": False},
        verify=False,
        timeout=5
    )
    response.raise_for_status()
    log.debug("Authentication endpoint responded %s", response.text)
    log.debug("Authentication endpoint send cookies %s", str(response.cookies))
    return {"AuthCookie": response.cookies["AuthCookie"], "UserRecord": response.cookies["UserRecord"]}


def read_soc(address: str, cookie) -> float:
    response = requests.get("https://" + address + "/api/system_status/soe", cookies=cookie, verify=False, timeout=5)
    response.raise_for_status()
    log.debug("SoC-Response: %s", response.text)
    return response.json()["percentage"]


def read_aggregate(address: str, cookie):
    response = requests.get("https://" + address + "/api/meters/aggregates", cookies=cookie, verify=False, timeout=5)
    response.raise_for_status()
    return response.json()


def update_using_cookie(address: str, cookie):
    aggregate = read_aggregate(address, cookie)
    get_bat_value_store(1).set(BatState(
        imported=aggregate["battery"]["energy_imported"],
        exported=aggregate["battery"]["energy_exported"],
        power=-aggregate["battery"]["instant_power"],
        soc=read_soc(address, cookie)
    ))


def authenticate_and_update(address: str, password: str):
    cookie = authenticate(address, password)
    COOKIE_FILE.write_text(json.dumps(cookie))
    update_using_cookie(address, cookie)


def update(address: str, password: str):
    log.debug("Beginning update")
    cookies = None
    try:
        cookies = json.loads(COOKIE_FILE.read_text())
    except FileNotFoundError:
        log.debug("Cookie-File <%s> does not exist. It will be created.", COOKIE_FILE)
    except JSONDecodeError as e:
        log.warning("Could not parse Cookie-File <%s>. It will be re-created.", COOKIE_FILE, exc_info=e)

    if cookies is None:
        authenticate_and_update(address, password)
        return
    try:
        update_using_cookie(address, cookies)
        return
    except HTTPError as e:
        if e.response.status_code != 401 and e.response.status_code != 403:
            raise e
        log.warning("Login to powerwall with existing cookie failed. Will retry with new cookie...")
    authenticate_and_update(address, password)
    log.debug("Update completed successfully")


if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(update)
