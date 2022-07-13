#!/usr/bin/env python3
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Sunny Boy Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class SmaSunnyBoyCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        with self.__tcp_client:
            imp = self.__tcp_client.read_holding_registers(30865, ModbusDataType.UINT_32, unit=3)
            exp = self.__tcp_client.read_holding_registers(30867, ModbusDataType.UINT_32, unit=3)
            if imp > 5:
                power = imp
            else:
                power = exp * -1

        topic_str = "openWB/set/system/device/{}/component/{}/".format(self.__device_id, self.component_config["id"])
        imported, exported = self.__sim_count.sim_count(power, topic=topic_str, data=self.simulation, prefix="bezug")

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)
