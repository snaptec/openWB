#!/usr/bin/env python3
import logging
from typing import Dict, Optional, Union, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext, SingleComponentUpdateContext
from modules.common.store import get_inverter_value_store
from modules.devices.fronius import bat
from modules.devices.fronius import counter_s0
from modules.devices.fronius import counter_sm
from modules.devices.fronius import inverter
from modules.devices.fronius.config import (Fronius, FroniusBatSetup, FroniusSmCounterSetup, FroniusS0CounterSetup,
                                            FroniusInverterSetup)

log = logging.getLogger(__name__)

fronius_component_classes = Union[bat.FroniusBat, counter_sm.FroniusSmCounter,
                                  counter_s0.FroniusS0Counter, inverter.FroniusInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.FroniusBat,
        "counter_sm": counter_sm.FroniusSmCounter,
        "counter_s0": counter_s0.FroniusS0Counter,
        "inverter": inverter.FroniusInverter,
    }

    def __init__(self, device_config: Union[Dict, Fronius]) -> None:
        self.components = {}  # type: Dict[str, fronius_component_classes]
        try:
            self.device_config = dataclass_from_dict(Fronius, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict,
                                                    FroniusBatSetup,
                                                    FroniusSmCounterSetup,
                                                    FroniusS0CounterSetup,
                                                    FroniusInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.device_config.configuration)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with MultiComponentUpdateContext(self.components):
                for component in self.components:
                    self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter_sm": counter_sm,
    "counter_s0": counter_s0,
    "inverter": inverter,
}


def read_legacy(
        component_type: str,
        ip_address: str,
        meter_id: int,
        variant: int,
        ip_address2: str = "none",
        num: Optional[int] = None) -> None:

    device_config = Fronius()
    device_config.configuration.ip_address = ip_address
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
        if component_type == "bat":
            component_config.configuration.meter_id = meter_id
        elif component_type == "counter_sm":
            component_config.configuration.variant = variant
            component_config.configuration.meter_id = meter_id
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)

    log.debug('Fronius IP-Adresse: ' + ip_address)

    if component_type == "bat" or "counter" in component_type:
        dev.update()
    elif component_type == "inverter" and num:
        inverter1 = inverter.FroniusInverter(num, component_config, dev.device_config.configuration)
        with SingleComponentUpdateContext(inverter1.component_info):
            total_power = inverter1.read_power()
            if ip_address2 != "none":
                dev.device_config.configuration.ip_address = ip_address2
                inverter2 = inverter.FroniusInverter(num, component_config, dev.device_config.configuration)
                total_power += inverter2.read_power()
            get_inverter_value_store(num).set(inverter1.fill_inverter_state(total_power))
    else:
        raise Exception("illegal component num " + str(num) + ". Should be an int if it is an inverter.")


def main(argv: List[str]) -> None:
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Fronius)
