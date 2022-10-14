# !/usr/bin/env python3
from enum import IntEnum
from itertools import chain
from typing import Any, Callable, Iterable, List, Union
from pymodbus.constants import Endian
from ipparser import ipparser
import logging
import functools
from modules.common.component_state import InverterState

from modules.kostal_plenticore.inverter import KostalPlenticoreInverter
from modules.kostal_plenticore.counter import KostalPlenticoreCounter
from modules.kostal_plenticore.config import (KostalPlenticore, KostalPlenticoreBatSetup, KostalPlenticoreCounterSetup,
                                              KostalPlenticoreInverterSetup)
from modules.kostal_plenticore.bat import KostalPlenticoreBat
from modules.common.store import get_counter_value_store
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.common.abstract_device import DeviceDescriptor
from modules.common import modbus
from helpermodules.cli import run_using_positional_cli_args


log = logging.getLogger(__name__)


class LegacyCounterPosition(IntEnum):
    HOME_CONSUMPTION = 0
    GRID = 1


def update(
        components: Iterable[Union[KostalPlenticoreBat, KostalPlenticoreCounter, KostalPlenticoreInverter]],
        reader: Callable[[int, modbus.ModbusDataType], Any]):
    request_components(components, reader)


def request_components(
        components: Iterable[Union[KostalPlenticoreBat, KostalPlenticoreCounter, KostalPlenticoreInverter]],
        reader: Callable[[int, modbus.ModbusDataType], Any],
        set_inverter_state: bool = True):
    battery = next((component for component in components if isinstance(component, KostalPlenticoreBat)), None)
    bat_state = battery.update() if battery else None
    for component in components:
        if isinstance(component, KostalPlenticoreInverter):
            inverter_state = component.update(reader)
            if bat_state:
                dc_in = component.dc_in_string_1_2(reader)
                home_consumption = component.home_consumption(reader)
                if dc_in >= 0:
                    # Wird PV-DC-Leistung erzeugt, müssen die Wandlungsverluste betrachtet werden.
                    # Kostal liefert nur DC-seitige Werte.
                    if bat_state.power > 0:
                        # Wird die Batterie entladen, werden die Wandlungsverluste anteilig an der DC-Leistung auf PV
                        # und Batterie verteilt. Dazu muss der Divisor Total_DC_power != 0 sein.
                        raw_inv_power = inverter_state.power
                        inverter_state.power = dc_in / (dc_in + bat_state.power) * raw_inv_power
                        # Speicherladung muss durch Wandlungsverluste und internen Verbrauch korrigiert werden, sonst
                        # wird ein falscher Hausverbrauch berechnet. Die Verluste fallen hier unter den Tisch.
                        bat_state.power = - raw_inv_power + inverter_state.power - home_consumption
                    else:
                        # Wenn die Batterie geladen wird, dann ist PV-Leistung die Wechselrichter-AC-Leistung + die
                        # Ladeleistung der Batterie. Die PV-Leistung ist die Summe aus verlustbehafteter
                        # AC-Leistungsabgabe des WR und der DC-Ladeleistung. Die Wandlungsverluste werden also nur
                        # in der PV-Leistung ersichtlich.
                        inverter_state.power += bat_state.power
            if set_inverter_state:
                component.set(inverter_state)
        elif isinstance(component, KostalPlenticoreCounter):
            component.update(reader)
    if bat_state:
        for component in components:
            if isinstance(component, KostalPlenticoreBat):
                component.set(bat_state)
    if set_inverter_state is False:
        return inverter_state


def create_device(device_config: KostalPlenticore):
    def create_bat_component(component_config):
        return KostalPlenticoreBat(device_config.id, component_config)

    def create_counter_component(component_config):
        return KostalPlenticoreCounter(device_config.id, component_config)

    def create_inverter_component(component_config):
        return KostalPlenticoreInverter(component_config)

    def update_components(
        components: Iterable[Union[KostalPlenticoreBat, KostalPlenticoreCounter, KostalPlenticoreInverter]]
    ):
        with tcp_client:
            update(components, reader)

    tcp_client = modbus.ModbusTcpClient_(device_config.configuration.ip_address, 1502)
    reader = functools.partial(tcp_client.read_holding_registers, unit=71, wordorder=Endian.Little)
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component, counter=create_counter_component, inverter=create_inverter_component),
        component_updater=MultiComponentUpdater(update_components),
    )


def _create_reader(tcp_client: modbus.ModbusTcpClient_) -> Callable[[int, modbus.ModbusDataType], Any]:
    def little_endian_wordorder_reader(register: int, data_type: modbus.ModbusDataType):
        return tcp_client.read_holding_registers(
            register, data_type, unit=71, wordorder=Endian.Little)
    return little_endian_wordorder_reader


def read_legacy_inverter(ip1: str, ip2: str, battery: int, ip3: str, position: int) -> InverterState:
    # in IP3 kann ein aufeinanderfolgende Liste enthalten sein "192.168.0.1-3"
    log.debug("Kostal Plenticore: WR1: {}, WR2: {}, Battery: {}, WR3: {}".format(ip1, ip2, battery, ip3))
    additional_ips = [filter("none".__ne__, chain([ip2], ipparser(ip3)))]
    client_1 = modbus.ModbusTcpClient_(ip1, 1502)
    reader_1 = _create_reader(client_1)
    with client_1:
        components = [KostalPlenticoreInverter(KostalPlenticoreInverterSetup(id=1))]
        if battery:
            components.append(KostalPlenticoreBat(None, KostalPlenticoreBatSetup()))
        inverter_state = request_components(components, reader_1, set_inverter_state=False)

    for ip in additional_ips:
        client = modbus.ModbusTcpClient_(ip, 1502)
        with client:
            inverter_state_temp = KostalPlenticoreInverter(
                KostalPlenticoreInverterSetup(id=1)).update(_create_reader(client))
        inverter_state.power += inverter_state_temp.power
        inverter_state.exported += inverter_state_temp.exported
    components[1].set(inverter_state)
    return inverter_state


def read_legacy_counter(ip1: str, ip2: str, battery: int, ip3: str, position: int) -> None:
    log.debug("Kostal Plenticore: WR1: {}, Position: {}".format(ip1, position))
    client_1 = modbus.ModbusTcpClient_(ip1, 1502)
    reader_1 = _create_reader(client_1)
    counter_component = KostalPlenticoreCounter(None, KostalPlenticoreCounterSetup(id=None))
    if LegacyCounterPosition(position) == LegacyCounterPosition.GRID:
        with client_1:
            counter_component.update(reader_1)
    else:
        with client_1:
            counter_state = counter_component.get_values(reader_1)
            bat_power = KostalPlenticoreBat(None, KostalPlenticoreBatSetup()).update(reader_1).power
        inverter_power = read_legacy_inverter(ip1, ip2, battery, ip3, position).power
        counter_state.power += inverter_power + bat_power
        counter_state = counter_component.get_imported_exported(counter_state)
        get_counter_value_store(None).set(counter_state)


def main(argv: List[str]):
    run_using_positional_cli_args({"counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
                                  )


device_descriptor = DeviceDescriptor(configuration_factory=KostalPlenticore)
