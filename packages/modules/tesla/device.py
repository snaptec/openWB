#!/usr/bin/env python3
import json
import logging
import requests
from json import JSONDecodeError
from requests import HTTPError
from typing import Callable, Dict, Union, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.req import get_http_session
from modules.common.store import RAMDISK_PATH
from modules.tesla import bat
from modules.tesla import counter
from modules.tesla import inverter
from modules.tesla.http_client import PowerwallHttpClient

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "Tesla",
        "type": "tesla",
        "id": 0,
        "configuration": {
            "ip_address": None,
            "email": None,
            "password": None
        }
    }


class TeslaConfiguration:
    def __init__(self, ip_address: str, email: str, password: str):
        self.ip_address = ip_address
        self.email = email
        self.password = password

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["ip_address", "email", "password"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return TeslaConfiguration(*values)


class Tesla:
    def __init__(self, name: str, type: str, id: int, configuration: TeslaConfiguration) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["name", "type", "id", "configuration"]
        try:
            values = [device_config[key] for key in keys]
            values = []
            for key in keys:
                if isinstance(device_config[key], Dict):
                    values.append(TeslaConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return Tesla(*values)


UpdateFunction = Callable[[PowerwallHttpClient], None]
COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
tesla_component_classes = Union[bat.TeslaBat, counter.TeslaCounter, inverter.TeslaInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.TeslaBat,
        "counter": counter.TeslaCounter,
        "inverter": inverter.TeslaInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, tesla_component_classes]
        try:
            self.config = device_config \
                if isinstance(device_config, Tesla) \
                else Tesla.from_dict(device_config)
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Beginning update")
        cookies = None
        address = self.config.configuration.ip_address
        email = self.config.configuration.email
        password = self.config.configuration.password
        with MultiComponentUpdateContext(self._components):
            try:
                cookies = json.loads(COOKIE_FILE.read_text())
            except FileNotFoundError:
                log.debug("Cookie-File <%s> does not exist. It will be created.", COOKIE_FILE)
            except JSONDecodeError:
                log.warning("Could not parse Cookie-File "+str(COOKIE_FILE)+". It will be re-created.", exc_info=True)

            session = get_http_session()
            if cookies is None:
                self.__authenticate_and_update(session, address, email, password, self.__update_components)
                return
            try:
                self.__update_components(PowerwallHttpClient(address, session, cookies))
                return
            except HTTPError as e:
                if e.response.status_code != 401 and e.response.status_code != 403:
                    raise e
                log.warning(
                    "Login to powerwall with existing cookie failed. Will retry with new cookie...")
            self.__authenticate_and_update(session, address, email, password, self.__update_components)
            log.debug("Update completed successfully")

    def __update_components(self, client: PowerwallHttpClient):
        if self._components:
            for component in self._components:
                # read aggregate
                aggregate = client.get_json("/api/meters/aggregates")
                self._components[component].update(client, aggregate)
        else:
            log.warning(
                self.config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )

    def __authenticate(self, session: requests.Session, url: str, email: str, password: str):
        """
        email is not yet required for login (2022/01), but we simulate the whole login page
        """
        response = session.post(
            "https://" + url + "/api/login/Basic",
            json={"username": "customer", "email": email, "password": password, "force_sm_off": False},
            verify=False,
            timeout=5
        )
        log.debug("Authentication endpoint send cookies %s", str(response.cookies))
        return {"AuthCookie": response.cookies["AuthCookie"], "UserRecord": response.cookies["UserRecord"]}

    def __authenticate_and_update(self,
                                  session: requests.Session,
                                  address: str,
                                  email: str,
                                  password: str,
                                  update_function: UpdateFunction):
        cookie = self.__authenticate(session, address, email, password)
        COOKIE_FILE.write_text(json.dumps(cookie))
        update_function(PowerwallHttpClient(address, session, cookie))


def read_legacy(component_type: str,
                address: str,
                email: str,
                password: str,
                num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    device_config.update({"configuration": {
        "ip_address": address,
        "email": email,
        "password": password
    }})
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    dev.add_component(component_config)

    log.debug('Tesla Powerwall IP-Adresse: ' + address)
    log.debug('Tesla Powerwall Mail-Adresse: ' + email)
    log.debug('Tesla Powerwall Passwort: ' + password)

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
