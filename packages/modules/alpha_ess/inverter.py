#!/usr/bin/env python3
from typing import Dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Number
from modules.common.store import get_inverter_value_store

from modules.alpha_ess.config import AlphaEssConfiguration, AlphaEssInverterSetup
from dataclass_utils import dataclass_from_dict


class AlphaEssInverter:
    def __init__(self, device_id: int,
                 component_config: Dict,
                 tcp_client: modbus.ModbusTcpClient_,
                 device_config: AlphaEssConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(AlphaEssInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)
        self.__device_config = device_config

    def update(self, unit_id: int) -> None:
        reg_p = self.__version_factory()
        power = self.__get_power(unit_id, reg_p)

        topic_str = "openWB/set/system/device/" + \
            str(self.__device_id)+"/component/" + \
            str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(power,
                                                 topic=topic_str,
                                                 data=self.simulation,
                                                 prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.__store.set(inverter_state)

    def __version_factory(self) -> int:
        if self.__device_config.source == 0 and self.__device_config.version == 0:
            return 0x0012
        else:
            return 0x00A1

    def __get_power(self, unit: int, reg_p: int) -> Number:
        with self.__tcp_client:
            powers = [
                self.__tcp_client.read_holding_registers(address, ModbusDataType.INT_32, unit=unit)
                for address in [reg_p, 0x041F, 0x0423, 0x0427]
            ]
        powers[0] = abs(powers[0])
        power = sum(powers) * -1
        return power


component_descriptor = ComponentDescriptor(configuration_factory=AlphaEssInverterSetup)
