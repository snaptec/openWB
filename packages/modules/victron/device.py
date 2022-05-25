#!/usr/bin/env python3
import logging
from typing import Dict, Optional, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.victron import bat
from modules.victron import counter
from modules.victron import inverter

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "Victron",
        "type": "victron",
        "id": 0,
        "configuration": {
            "ip_address": None
        }
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.VictronBat,
        "counter": counter.VictronCounter,
        "inverter": inverter.VictronInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, Union[bat.VictronBat, counter.VictronCounter]]
        try:
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusClient(ip_address, 502)
            self.device_config = device_config
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (
                self.COMPONENT_TYPE_TO_CLASS[component_type](self.device_config["id"], component_config, self.client))
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
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(
        component_type: str,
        ip_address: str,
        modbus_id: Optional[int] = 100,
        energy_meter: Optional[int] = 1,
        mppt: Optional[int] = 0,
        num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }

    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    dev = Device(device_config)

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        if component_type == "counter":
            component_config["configuration"]["energy_meter"] = bool(energy_meter)
        elif component_type == "inverter":
            component_config["configuration"]["mppt"] = mppt
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    component_config["configuration"]["modbus_id"] = modbus_id
    dev.add_component(component_config)

    log.debug('Victron IP-Adresse: ' + ip_address)
    log.debug('Victron Energy Meter: ' + str(bool(energy_meter)))
    log.debug('Victron Modbus-ID: ' + str(modbus_id))
    log.debug('Victron MPPT: ' + str(mppt))
    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
