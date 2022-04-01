#!/usr/bin/env python3
import logging

from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA ModbusTCP Wechselrichter",
        "id": 0,
        "type": "inverter_modbus_tcp",
        "configuration": {}
    }


log = logging.getLogger("SMA ModbusTCP")


class SmaModbusTcpInverter:

    SMA_INT32_NAN = -0x80000000  # SMA uses this value to represent NaN

    def __init__(self, device_address: str, component_config: dict) -> None:
        self.component_config = component_config
        self.__tcp_client = modbus.ModbusClient(device_address)
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        self.__store.set(self.read_inverter_state())

    def read_inverter_state(self) -> InverterState:
        log.debug("Komponente "+self.component_config["name"]+" auslesen.")
        with self.__tcp_client:
            # AC Wirkleistung über alle Phasen (W) [Pac]:
            power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=3)
            if power == self.SMA_INT32_NAN:
                power = 0
            # Gesamtertrag (Wh) [E-Total]:
            energy = self.__tcp_client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)

            return InverterState(
                power=-max(power, 0),
                counter=energy
            )
