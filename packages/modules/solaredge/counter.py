#!/usr/bin/env python3
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.solaredge.scale import scale_registers


def get_default_config() -> dict:
    return {
        "name": "SolarEdge Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {
            "modbus_id": 1
        }
    }


class SolaredgeCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        with self.__tcp_client:
            def read_scaled_int16(address: int, count: int):
                return scale_registers(
                    self.__tcp_client.read_holding_registers(
                        address,
                        [ModbusDataType.INT_16] * (count+1),
                        unit=self.component_config["configuration"]["modbus_id"])
                )

            # 40206: Total Real Power (sum of active phases)
            # 40206/40207/40208: Real Power by phase
            # 40210: AC Real Power Scale Factor
            powers = [-power for power in read_scaled_int16(40206, 4)]

            # 40191/40192/40193: AC Current by phase
            # 40194: AC Current Scale Factor
            currents = read_scaled_int16(40191, 3)

            # 40196/40197/40198: Voltage per phase
            # 40203: AC Voltage Scale Factor
            voltages = read_scaled_int16(40196, 7)[:3]

            # 40204: AC Frequency
            # 40205: AC Frequency Scale Factor
            frequency = read_scaled_int16(40204, 1)[0]

            # 40222/40223/40224: Power factor by phase (unit=%)
            # 40225: AC Power Factor Scale Factor
            power_factors = [power_factor / 100 for power_factor in read_scaled_int16(40222, 3)]

            # 40234: Total Imported Real Energy
            counter_imported = self.__tcp_client.read_holding_registers(
                40234, ModbusDataType.UINT_32, unit=self.component_config["configuration"]["modbus_id"])

            # 40226: Total Exported Real Energy
            counter_exported = self.__tcp_client.read_holding_registers(
                40226, ModbusDataType.UINT_32, unit=self.component_config["configuration"]["modbus_id"])

        counter_state = CounterState(
            imported=counter_imported,
            exported=counter_exported,
            power=powers[0],
            powers=powers[1:],
            voltages=voltages,
            currents=currents,
            power_factors=power_factors,
            frequency=frequency
        )
        self.__store.set(counter_state)
