#!/usr/bin/env python3
import itertools
import logging
from typing import Dict, Union, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.sma_modbus_tcp import inverter_modbus_tcp
from modules.sma_modbus_tcp import inverter_webbox
from modules.sma_modbus_tcp.inverter_version import SmaInverterVersion
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.store import get_inverter_value_store
from modules.sma_modbus_tcp.config import (SmaModbusTcp, SmaModbusTcpInverterConfiguration, SmaModbusTcpInverterSetup,
                                           SmaWebboxInverterSetup)

log = logging.getLogger(__name__)


sma_modbus_tcp_component_classes = Union[
    inverter_webbox.SmaWebboxInverter,
    inverter_modbus_tcp.SmaModbusTcpInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "inverter_modbus_tcp": inverter_modbus_tcp.SmaModbusTcpInverter,
        "inverter_webbox": inverter_webbox.SmaWebboxInverter
    }
    COMPONENT_TYPE_TO_MODULE = {
        "inverter_modbus_tcp": inverter_modbus_tcp,
        "inverter_webbox": inverter_webbox
    }

    def __init__(self, device_config: Union[Dict, SmaModbusTcp]) -> None:
        self.components = {}  # type: Dict[str, sma_modbus_tcp_component_classes]
        try:
            self.device_config = dataclass_from_dict(SmaModbusTcp, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict, SmaModbusTcpInverterSetup, SmaWebboxInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(self.COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                self.device_config.configuration.ip_address,
                component_config)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components.values():
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(component.component_info):
                    component.update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(ip1: str, webbox: int, ip2: str, ip3: str, ip4: str, version: int, hybrid: int, num: int) -> None:
    def create_webbox_inverter(address: str):
        config = SmaWebboxInverterSetup(id=num)
        return inverter_webbox.SmaWebboxInverter(0, address, config)

    def create_modbus_inverter(address: str):
        config = SmaModbusTcpInverterSetup(id=num, configuration=SmaModbusTcpInverterConfiguration(
            version=SmaInverterVersion(version), hybrid=bool(hybrid)))
        return inverter_modbus_tcp.SmaModbusTcpInverter(0, address, config)

    inverter1 = (create_webbox_inverter if webbox else create_modbus_inverter)(ip1)
    inverters_additional = (create_modbus_inverter(address) for address in [ip2, ip3, ip4] if address != "none")
    # In legacy we were able to configure multiple IP-Addresses for a single SMA-component, effectively creating a
    # virtual component that represents the sum of its subcomponents. This was probably done in order to circumvent
    # the limitation to have a maximum of two inverters configured in legacy.
    # Since openWB 2 does not have a limitation on the number of inverters we do not implement this there. However
    # we still need to implement this for the read_legacy-bridge.
    # Here we act like we only update the first inverter, while we actually query all inverters and sum them up:
    with SingleComponentUpdateContext(inverter1.component_info):
        total_power = 0
        total_energy = 0
        for inverter in itertools.chain((inverter1,), inverters_additional):
            state = inverter.read_inverter_state()
            total_power += state.power
            total_energy += state.exported
        get_inverter_value_store(num).set(InverterState(exported=total_energy, power=total_power))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SmaModbusTcp)
