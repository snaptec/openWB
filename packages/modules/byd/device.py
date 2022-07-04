#!/usr/bin/env python3
import logging
from typing import Dict, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.byd import bat
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "BYD",
        "type": "byd",
        "id": 0,
        "configuration": {
            "ip_address": None,
            "username": None,
            "password": None
        }
    }


class BYDConfiguration:
    def __init__(self, ip_address: str, username: str, password: str):
        self.ip_address = ip_address
        self.username = username
        self.password = password

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["ip_address", "username", "password"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return BYDConfiguration(*values)


class BYD:
    def __init__(self, name: str, type: str, id: int, configuration: BYDConfiguration) -> None:
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
                    values.append(BYDConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return BYD(*values)


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.BYDBat
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, bat.BYDBat]
        try:
            self.device_config = device_config \
                if isinstance(device_config, BYD) \
                else BYD.from_dict(device_config)
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config,
                self.device_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, ip_address: str, username: str, password: str,  num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat
    }
    device_config = get_default_config()
    device_config["configuration"]["username"] = username
    device_config["configuration"]["password"] = password
    device_config["configuration"]["ip_address"] = ip_address
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

    log.debug('byd IP-Adresse: ' + ip_address)
    log.debug('byd Benutzer: ' + username)
    log.debug('byd Passwort: ' + password)

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
