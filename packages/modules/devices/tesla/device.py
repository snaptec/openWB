#!/usr/bin/env python3
import json
import logging
import requests
from json import JSONDecodeError
from requests import HTTPError
from typing import Callable, Dict, Union, Optional, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.req import get_http_session
from modules.common.store import RAMDISK_PATH
from modules.devices.tesla import bat, counter, inverter
from modules.devices.tesla.config import Tesla, TeslaBatSetup, TeslaCounterSetup, TeslaInverterSetup
from modules.devices.tesla.http_client import PowerwallHttpClient

log = logging.getLogger(__name__)


UpdateFunction = Callable[[PowerwallHttpClient], None]
COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
tesla_component_classes = Union[bat.TeslaBat, counter.TeslaCounter, inverter.TeslaInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.TeslaBat,
        "counter": counter.TeslaCounter,
        "inverter": inverter.TeslaInverter
    }

    def __init__(self, device_config: Union[Dict, Tesla]) -> None:
        self.components = {}  # type: Dict[str, tesla_component_classes]
        try:
            self.device_config = dataclass_from_dict(Tesla, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict,
                                                    TeslaBatSetup,
                                                    TeslaCounterSetup,
                                                    TeslaInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Beginning update")
        cookies = None
        address = self.device_config.configuration.ip_address
        email = self.device_config.configuration.email
        password = self.device_config.configuration.password
        with MultiComponentUpdateContext(self.components):
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
        if self.components:
            for component in self.components:
                # read aggregate
                aggregate = client.get_json("/api/meters/aggregates")
                self.components[component].update(client, aggregate)
        else:
            log.warning(
                self.device_config.name +
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


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                address: str,
                email: str,
                password: str,
                num: Optional[int] = None) -> None:
    device_config = Tesla()
    device_config.configuration.ip_address = address
    device_config.configuration.email = email
    device_config.configuration.password = password

    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)

    log.debug('Tesla Powerwall IP-Adresse: ' + address)
    log.debug('Tesla Powerwall Mail-Adresse: ' + email)
    log.debug('Tesla Powerwall Passwort: ' + password)

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Tesla)
