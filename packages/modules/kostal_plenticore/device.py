#!/usr/bin/env python3
import logging
from ipparser import ipparser
from pymodbus.constants import Endian
from typing import Any, Callable, Iterable, List, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.kostal_plenticore import bat, counter, inverter
from modules.kostal_plenticore.bat import KostalPlenticoreBat
from modules.kostal_plenticore.config import (KostalPlenticore, KostalPlenticoreBatSetup, KostalPlenticoreCounterSetup,
                                              KostalPlenticoreInverterSetup)
from modules.kostal_plenticore.counter import KostalPlenticoreCounter
from modules.kostal_plenticore.inverter import KostalPlenticoreInverter

log = logging.getLogger(__name__)


def update_components(
        components: Iterable[Union[KostalPlenticoreBat, KostalPlenticoreCounter, KostalPlenticoreInverter]]):
    with tcp_client:
        for component in components:
            if isinstance(component, KostalPlenticoreBat):
                bat_state = component.update()
        else:
            bat_state = None
        for component in components:
            if isinstance(component, KostalPlenticoreInverter):
                inverter_state = component.update()
                if bat_state:
                    dc_in = component.dc_in_string_1_2()
                    home_consumption = component.home_consumption()
                    if dc_in >= 0:
                        if bat_state.power > 0:
                            raw_inv_power = inverter_state.power
                            inverter_state.power = dc_in / (dc_in + bat_state.power) * raw_inv_power
                            bat_state.power = raw_inv_power - inverter_state.power - home_consumption
                        else:
                            inverter_state.power -= bat_state.power
                component.set(inverter_state)
            else:
                component.update()
        if bat_state:
            for component in components:
                if isinstance(component, KostalPlenticoreBat):
                    component.set(bat_state)


def create_device(device_config: KostalPlenticore):
    def create_bat_component(component_config):
        return KostalPlenticoreBat(device_config.id, component_config, reader)

    def create_counter_component(component_config):
        return KostalPlenticoreCounter(device_config.id, component_config, reader)

    def create_inverter_component(component_config):
        return KostalPlenticoreInverter(component_config, reader)

    def little_endian_wordorder_reader(register: int, data_type: modbus.ModbusDataType):
        return tcp_client.read_holding_registers(
            register, data_type, unit=71, wordorder=Endian.Little)
    reader = little_endian_wordorder_reader

    tcp_client = modbus.ModbusTcpClient_(device_config.configuration.ip_address, 1502)
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component, counter=create_counter_component, inverter=create_inverter_component),
        component_updater=MultiComponentUpdater(update_components),
    )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str, ip1: str, ip2: str, battery: int, ip3: str) -> None:
    def create_reader(tcp_client: modbus.ModbusTcpClient_) -> Callable[[int, modbus.ModbusDataType], Any]:
        def little_endian_wordorder_reader(register: int, data_type: modbus.ModbusDataType):
            return tcp_client.read_holding_registers(
                register, data_type, unit=71, wordorder=Endian.Little)
        return little_endian_wordorder_reader
    ip4, ip5 = None, None
    ips = ipparser(ip3)
    # in IP3 kann ein aufeinanderfolgende Liste enthalten sein "192.168.0.1-3"
    if len(ips) > 1:
        ip3 = ips[0]
        ip4 = ips[1]
        ip5 = ips[2]

    client_1 = modbus.ModbusTcpClient_(ip1, 1502)
    reader_1 = create_reader(client_1)
    if component_type == "inverter":
        with client_1:
            inv_component = KostalPlenticoreInverter(KostalPlenticoreInverterSetup(id=1))
            inverter_state = inv_component.update(reader_1)
            if battery:
                bat_component = KostalPlenticoreBat(KostalPlenticoreBatSetup())
                dc_in = inv_component.dc_in_string_1_2(reader_1)
                home_consumption = inv_component.home_consumption(reader_1)
                bat_state = bat_component.update(reader_1)
                if dc_in >= 0:
                    if bat_state.power > 0:
                        raw_inv_power = inverter_state.power
                        inverter_state.power = dc_in / (dc_in + bat_state.power) * raw_inv_power
                        bat_state.power = raw_inv_power - inverter_state.power - home_consumption
                    else:
                        inverter_state.power -= bat_state.power
                bat_component.set(bat_state)

        inverter_ips = list(map(str,
                                filter(lambda ip: ip is not None and ip != "none",
                                       [ip2, ip3, ip4, ip5])))
        for ip in inverter_ips:
            client = modbus.ModbusTcpClient_(ip, 1502)
            with client:
                inverter_state_temp = inv_component.update(create_reader(client))
            inverter_state.power += inverter_state_temp.power
            inverter_state.exported += inverter_state_temp.exported
        inv_component.set(inverter_state)
    elif component_type == "counter":
        with client_1:
            KostalPlenticoreCounter(KostalPlenticoreCounterSetup(id=None)).update(reader_1)

    log.debug("Kostal Plenticore: WR1: {}, WR2: {}, Battery: {}, WR3: {}, WR4:, {}, WR5: {}".format(
        ip1, ip2, battery, ip3, ip4, ip5))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=KostalPlenticore)
