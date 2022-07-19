#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.victron.config import VictronCounterSetup


class VictronCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, VictronCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(VictronCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        unit = self.component_config.configuration.modbus_id
        energy_meter = self.component_config.configuration.energy_meter
        with self.__tcp_client:
            if energy_meter:
                powers = self.__tcp_client.read_holding_registers(2600, [ModbusDataType.INT_16]*3, unit=unit)
                currents = [
                    self.__tcp_client.read_holding_registers(reg, ModbusDataType.INT_16, unit=unit) / 10
                    for reg in [2617, 2619, 2621]]
                voltages = [
                    self.__tcp_client.read_holding_registers(reg, ModbusDataType.UINT_16, unit=unit) / 10
                    for reg in [2616, 2618, 2620]]
                power = sum(powers)
            else:
                powers = self.__tcp_client.read_holding_registers(820, [ModbusDataType.INT_16]*3, unit=unit)
                power = sum(powers)

        topic_str = "openWB/set/system/device/{}/component/{}/".format(
            self.__device_id, self.component_config.id
        )
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )

        if energy_meter:
            counter_state = CounterState(
                voltages=voltages,
                currents=currents,
                powers=powers,
                imported=imported,
                exported=exported,
                power=power
            )
        else:
            counter_state = CounterState(
                powers=powers,
                imported=imported,
                exported=exported,
                power=power
            )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=VictronCounterSetup)
