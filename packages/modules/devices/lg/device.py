#!/usr/bin/env python3
import json
import logging
import os
from typing import Dict, Union, Optional, List
from requests import HTTPError, Session

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.fault_state import FaultState
from modules.devices.lg.config import LG, LgBatSetup, LgConfiguration, LgCounterSetup, LgInverterSetup
from modules.devices.lg import bat, counter, inverter

log = logging.getLogger(__name__)


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

    def __init__(self, device_config: Union[Dict, LG]) -> None:
        self.components = {}  # type: Dict[str, lg_component_classes]
        self.session_key = " "
        try:
            self.device_config = dataclass_from_dict(LG, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict, LgBatSetup, LgCounterSetup, LgInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with MultiComponentUpdateContext(self.components):
                session = req.get_http_session()
                try:
                    response = self._request_data(session)
                except HTTPError:
                    self._update_session_key(session)
                    response = self._request_data(session)

                for component in self.components:
                    self.components[component].update(response)
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )

    def _update_session_key(self, session: Session):
        try:
            headers = {'Content-Type': 'application/json', }
            data = json.dumps({"password": self.device_config.configuration.password})
            response = session.put("https://"+self.device_config.configuration.ip_address+'/v1/login', headers=headers,
                                   data=data, verify=False, timeout=5).json()
            self.session_key = response["auth_key"]
        except (HTTPError, KeyError):
            raise FaultState.error("login failed! check password!")

    def _request_data(self, session: Session) -> Dict:
        headers = {'Content-Type': 'application/json', }
        data = json.dumps({"auth_key": self.session_key})
        return session.post("https://"+self.device_config.configuration.ip_address + "/v1/user/essinfo/home",
                            headers=headers,
                            data=data,
                            verify=False,
                            timeout=5).json()


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str, ip: str, password: str, num: Optional[int] = None) -> None:
    dev = Device(LG(configuration=LgConfiguration(ip_address=ip, password=password)))

    if os.path.isfile("/var/www/html/openWB/ramdisk/ess_session_key"):
        with open("/var/www/html/openWB/ramdisk/ess_session_key", "r") as f:
            # erste Zeile ohne Zeilenumbruch lesen
            old_session_key = f.readline().strip()
            dev.session_key = old_session_key
    else:
        old_session_key = dev.session_key

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    if component_type == "bat" or component_type == "counter":
        num = None
    component_config.id = num
    dev.add_component(component_config)
    log.debug('LG ESS V1.0 IP: ' + ip)
    log.debug('LG ESS V1.0 password: ' + password)
    dev.update()

    if dev.session_key != old_session_key:
        with open("/var/www/html/openWB/ramdisk/ess_session_key", "w") as f:
            f.write(str(dev.session_key))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=LG)
