#!/usr/bin/env python3

import json
import logging
from json import JSONDecodeError
import requests
from requests import HTTPError

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import CounterState
from modules.common.store import get_counter_value_store, RAMDISK_PATH

COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
log = logging.getLogger("Powerwall")


def authenticate(url: str, email: str, password: str):
    '''
    email is not yet required for login (2022/01), but we simulate the whole login page
    '''
    response = requests.post(
        "https://" + url + "/api/login/Basic",
        json={"username": "customer", "email": email, "password": password},
        verify=False,
        timeout=5
    )
    response.raise_for_status()
    log.debug("Authentication endpoint responded %s", response.text)
    log.debug("Authentication endpoint send cookies %s", str(response.cookies))
    return {"AuthCookie": response.cookies["AuthCookie"], "UserRecord": response.cookies["UserRecord"]}


def read_site(address: str, cookie):
    response = requests.get("https://" + address + "/api/meters/site", cookies=cookie, verify=False, timeout=5)
    response.raise_for_status()
    return response.json()


def read_status(address: str, cookie):
    response = requests.get("https://" + address + "/api/status", cookies=cookie, verify=False, timeout=5)
    response.raise_for_status()
    return response.json()


def read_aggregate(address: str, cookie):
    response = requests.get("https://" + address + "/api/meters/aggregates", cookies=cookie, verify=False, timeout=5)
    response.raise_for_status()
    return response.json()


def update_using_cookie(address: str, cookie):
    # read firmware version
    status = read_status(address, cookie)
    # since 21.44.1 tesla adds the commit hash '21.44.1 c58c2df3'
    # so we split by whitespace and take the first element for comparison
    firmwareversion = int(status["version"].split()[0])
    log.debug('Version: ' + str(firmwareversion))
    # read aggregate
    aggregate = read_aggregate(address, cookie)
    # read additional info if firmware supports
    if firmwareversion >= 20490:
        meters_site = read_site(address, cookie)
        get_counter_value_store(1).set(CounterState(
            imported = aggregate["site"]["energy_imported"],
            exported = aggregate["site"]["energy_exported"],
            power_all = aggregate["site"]["instant_power"],
            voltages = [
                meters_site["0"]["Cached_readings"]["v_l" + str(phase) + "n"] for phase in range (1,4)
            ],
            currents = [
                meters_site["0"]["Cached_readings"]["i_" + phase + "_current"] for phase in ["a", "b", "c"]
            ],
            powers = [
                meters_site["0"]["Cached_readings"]["real_power_" + phase] for phase in ["a", "b", "c"]
            ]
        ))
    else:
        get_counter_value_store(1).set(CounterState(
            imported = aggregate["site"]["energy_imported"],
            exported = aggregate["site"]["energy_exported"],
            power_all = aggregate["site"]["instant_power"]
        ))


def authenticate_and_update(address: str, email: str, password: str):
    cookie = authenticate(address, email, password)
    COOKIE_FILE.write_text(json.dumps(cookie))
    update_using_cookie(address, cookie)


def update(address: str, email: str, password: str):
    log.debug("Beginning update")
    cookies = None
    try:
        cookies = json.loads(COOKIE_FILE.read_text())
    except FileNotFoundError:
        log.debug("Cookie-File <%s> does not exist. It will be created.", COOKIE_FILE)
    except JSONDecodeError as e:
        log.warning("Could not parse Cookie-File <%s>. It will be re-created.", COOKIE_FILE, exc_info=e)

    if cookies is None:
        authenticate_and_update(address, email, password)
        return
    try:
        update_using_cookie(address, cookies)
        return
    except HTTPError as e:
        if e.response.status_code != 401 and e.response.status_code != 403:
            raise e
        log.warning("Login to powerwall with existing cookie failed. Will retry with new cookie...")
    authenticate_and_update(address, email, password)
    log.debug("Update completed successfully")


if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(update)
