#!/usr/bin/env python3
import json
import logging
import os
from typing import Dict, Union, Optional, List
from requests import HTTPError, Session

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.lg import bat
from modules.lg import counter
from modules.lg import inverter
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.fault_state import FaultState

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "LG ESS V1.0",
        "type": "lg",
        "id": 0,
        "configuration": {
            "ip": None,
            "password": None
        }
    }


class DeviceConfiguration:
    def __init__(self, ip_address: str, password: str):
        self.ip_address = ip_address
        self.password = password

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["ip_address", "password"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return DeviceConfiguration(*values)


class LG:
    def __init__(self, name: str, type: str, id: int, configuration: DeviceConfiguration) -> None:
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
                    values.append(DeviceConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return LG(*values)


lg_component_classes = Union[bat.LgBat, counter.LgCounter, inverter.LgInverter]


class Device(AbstractDevice):
    """Beispiel JSON-Objekte liegen im Ordner lgessv1/JSON-Beispiele.txt
    lg_ess_url:  IP/URL des LG ESS V1.0
    lg_ess_pass: Passwort, um sich in den LG ESS V1.0 einzuloggen.
                 Das Passwort ist standardmäßig die Registrierungsnummer,
                 die sich auf dem PCS (dem Hybridwechselrichter und
                 Batteriemanagementsystem) befindet (Aufkleber!). Alter-
                 nativ findet man die Registrierungsnummer in der App unter
                 dem Menüpunkt "Systeminformationen".
                 Mit der Registrierungsnummer kann man sich dann in der
                 Rolle "installer" einloggen."""
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.LgBat,
        "counter": counter.LgCounter,
        "inverter": inverter.LgInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, lg_component_classes]
        self.session_key = " "
        try:
            self.config = device_config \
                if isinstance(device_config, LG) \
                else LG.from_dict(device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.config.name)

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.config.id,
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self._components))
        if self._components:
            with MultiComponentUpdateContext(self._components):
                session = req.get_http_session()
                response = self._request_data(session)
                # missing "auth" in response indicates success
                if (response.get('auth') == "auth_key failed" or
                        response.get('auth') == "auth timeout" or
                        response.get('auth') == "not done"):
                    self._update_session_key(session)
                    response = self._request_data(session)

                for component in self._components:
                    self._components[component].update(response)
        else:
            log.warning(
                self.config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )

    def _update_session_key(self, session: Session):
        try:
            headers = {'Content-Type': 'application/json', }
            data = json.dumps({"password": self.config.configuration.password})
            response = session.put("https://"+self.config.configuration.ip_address+'/v1/login', headers=headers,
                                   data=data, verify=False, timeout=5).json()
            self.session_key = response["auth_key"]
        except (HTTPError, KeyError):
            raise FaultState.error("login failed! check password!")

    def _request_data(self, session: Session) -> Dict:
        headers = {'Content-Type': 'application/json', }
        data = json.dumps({"auth_key": self.session_key})
        return session.post("https://"+self.config.configuration.ip_address + "/v1/user/essinfo/home",
                            headers=headers,
                            data=data,
                            verify=False,
                            timeout=5).json()


def read_legacy(component_type: str, ip: str, password: str, num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip
    device_config["configuration"]["password"] = password
    dev = Device(device_config)

    if os.path.isfile("/var/www/html/openWB/ramdisk/ess_session_key"):
        with open("/var/www/html/openWB/ramdisk/ess_session_key", "r") as f:
            # erste Zeile ohne Zeilenumbruch lesen
            old_session_key = f.readline().strip()
            dev.session_key = old_session_key
    else:
        old_session_key = dev.session_key

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    dev.add_component(component_config)
    log.debug('LG ESS V1.0 IP: ' + ip)
    log.debug('LG ESS V1.0 password: ' + password)
    dev.update()

    if dev.session_key != old_session_key:
        with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
            f.write(str(dev.session_key))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
