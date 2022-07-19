#!/usr/bin/env python3
import itertools
import logging
from typing import Dict, Optional, Union, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store
from modules.sma_sunny_boy import bat, bat_smart_energy, counter, inverter
from modules.sma_sunny_boy.config import (SmaSunnyBoy, SmaSunnyBoyBatSetup, SmaSunnyBoyConfiguration,
                                          SmaSunnyBoyCounterSetup, SmaSunnyBoyInverterConfiguration,
                                          SmaSunnyBoyInverterSetup, SmaSunnyBoySmartEnergyBatSetup)
from modules.sma_sunny_boy.inverter_version import SmaInverterVersion
from modules.sma_webbox.config import SmaWebboxInverterSetup
from modules.sma_webbox.inverter import SmaWebboxInverter

log = logging.getLogger(__name__)


sma_modbus_tcp_component_classes = Union[
    bat.SunnyBoyBat,
    bat_smart_energy.SunnyBoySmartEnergyBat,
    counter.SmaSunnyBoyCounter,
    inverter.SmaSunnyBoyInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SunnyBoyBat,
        "bat_smart_energy": bat_smart_energy.SunnyBoySmartEnergyBat,
        "counter": counter.SmaSunnyBoyCounter,
        "inverter": inverter.SmaSunnyBoyInverter
    }

    def __init__(self, device_config: Union[Dict, SmaSunnyBoy]) -> None:
        self.components = {}  # type: Dict[str, sma_modbus_tcp_component_classes]
        try:
            self.device_config = dataclass_from_dict(SmaSunnyBoy, device_config)
            ip_address = self.device_config.configuration.ip_address
            self.client = modbus.ModbusTcpClient_(ip_address, 502)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict,
                                                    SmaSunnyBoyBatSetup,
                                                    SmaSunnyBoySmartEnergyBatSetup,
                                                    SmaSunnyBoyCounterSetup,
                                                    SmaSunnyBoyInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                component_config,
                self.client))
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


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "bat_smart_energy": bat_smart_energy,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                ip1: str,
                webbox: Optional[int] = None,
                ip2: Optional[str] = None,
                ip3: Optional[str] = None,
                ip4: Optional[str] = None,
                version: Optional[int] = None,
                hybrid: Optional[int] = None,
                sunny_boy_smart_energy: Optional[int] = None,
                num: Optional[int] = None) -> None:

    log.debug("SMA Modbus Ip-Adresse: "+ip1)
    log.debug("SMA Modbus Webbox: "+str(webbox))
    log.debug("SMA Modbus weitere IPs: "+str(ip2)+", "+str(ip3)+", "+str(ip4))
    log.debug("SMA Modbus Version: "+str(version))
    log.debug("SMA Modbus Hybrid: "+str(hybrid))
    if component_type in COMPONENT_TYPE_TO_MODULE:
        if component_type == "inverter":
            read_inverter(ip1, webbox, ip2, ip3, ip4, version, hybrid, num, sunny_boy_smart_energy)
            return
        else:
            component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
            component_config.id = None
            dev = Device(SmaSunnyBoy(configuration=SmaSunnyBoyConfiguration(ip_address=ip1)))
            dev.add_component(component_config)
            dev.update()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))


def read_inverter(ip1: str,
                  webbox: int,
                  ip2: str,
                  ip3: str,
                  ip4: str,
                  version: int,
                  hybrid: int,
                  num: int,
                  sunny_boy_smart_energy: int):
    def create_webbox_inverter(address: str):
        return SmaWebboxInverter(address, SmaWebboxInverterSetup(id=num))

    def create_modbus_inverter(address: str):
        config = SmaSunnyBoyInverterSetup(
            id=num,
            configuration=SmaSunnyBoyInverterConfiguration(hybrid=bool(hybrid),
                                                           version=SmaInverterVersion(version)))
        return inverter.SmaSunnyBoyInverter(0, config, modbus.ModbusTcpClient_(address, 502))

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
        for inv in itertools.chain((inverter1,), inverters_additional):
            state = inv.read()
            total_power += state.power
            total_energy += state.exported
        if hybrid == 1:
            if sunny_boy_smart_energy == 0:
                bat_comp = bat.SunnyBoyBat(0, SmaSunnyBoyBatSetup(), modbus.ModbusTcpClient_(ip1, 502))
            else:
                bat_comp = bat_smart_energy.SunnyBoySmartEnergyBat(0,
                                                                   SmaSunnyBoySmartEnergyBatSetup(),
                                                                   modbus.ModbusTcpClient_(ip1, 502))
            bat_state = bat_comp.read()
            total_power -= bat_state.power
            total_energy = total_energy+bat_state.imported-bat_state.exported
        get_inverter_value_store(num).set(InverterState(exported=total_energy, power=total_power))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SmaSunnyBoy)
