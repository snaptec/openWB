#!/usr/bin/env python3
import logging
from typing import Dict, Union, Optional, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.byd.config import BYD, BYDBatSetup, BYDConfiguration
from modules.byd.device import Device as BYDDevice
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.store import get_counter_value_store, get_inverter_value_store
from modules.common import simcount
from modules.common.component_state import CounterState, InverterState
from modules.kostal_piko.config import (KostalPiko,
                                        KostalPikoConfiguration,
                                        KostalPikoCounterSetup,
                                        KostalPikoInverterSetup)
from modules.kostal_piko import counter
from modules.kostal_piko import inverter

log = logging.getLogger(__name__)


kostal_piko_component_classes = Union[counter.KostalPikoCounter, inverter.KostalPikoInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "counter": counter.KostalPikoCounter,
        "inverter": inverter.KostalPikoInverter
    }

    def __init__(self, device_config: Union[Dict, KostalPiko]) -> None:
        self.components = {}  # type: Dict[str, kostal_piko_component_classes]
        try:
            self.device_config = dataclass_from_dict(KostalPiko, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict, KostalPikoCounterSetup, KostalPikoInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.device_config.configuration.ip_address))
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


COMPONENT_TYPE_TO_MODULE = {
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                address: str,
                bat_module: str,
                bat_ip: str,
                bat_username: str,
                bat_password: str,
                num: Optional[int] = None) -> None:
    dev = Device(KostalPiko(configuration=KostalPikoConfiguration(ip_address=address)))
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)

    log.debug('KostalPiko IP-Adresse: ' + address)
    log.debug('KostalPiko Speicher: ' + bat_module)

    if component_type == "inverter":
        with SingleComponentUpdateContext(dev.components["component"+str(num)].component_info):
            power, exported = dev.components["component"+str(num)].get_values()
            if bat_module == "speicher_bydhv":
                bat_power = _get_byd_bat_power(bat_ip, bat_username, bat_password, num)
                power -= bat_power
            get_inverter_value_store(num).set(InverterState(power=power, exported=exported))
    elif component_type == "counter":
        with SingleComponentUpdateContext(dev.components["componentNone"].component_info):
            home_consumption, powers = dev.components["componentNone"].get_values()
            if bat_module == "speicher_bydhv":
                bat_power = _get_byd_bat_power(bat_ip, bat_username, bat_password, num)
                home_consumption += bat_power

            dev.add_component(KostalPikoInverterSetup(id=num))
            inverter_power, _ = dev.components["component"+str(num)].get_values()

            power = home_consumption + inverter_power
            imported, exported = simcount.SimCountFactory().get_sim_counter(
            )().sim_count(power, topic="topic_str", data={}, prefix="bezug")
            counter_state = CounterState(
                imported=imported,
                exported=exported,
                power=power,
                powers=powers
            )
            get_counter_value_store(None).set(counter_state)


def _get_byd_bat_power(bat_ip: str, bat_username: str, bat_password: str, num: int) -> float:
    bat_dev = BYDDevice(BYD(configuration=BYDConfiguration(username=bat_username,
                                                           password=bat_password,
                                                           ip_address=bat_ip)))
    bat_dev.add_component(BYDBatSetup(id=num))
    bat_power, _ = bat_dev.components["component0"].get_values()
    return bat_power


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=KostalPiko)
