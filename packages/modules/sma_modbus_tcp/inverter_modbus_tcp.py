#!/usr/bin/env python3
import logging

from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.sma_modbus_tcp.inverter_version import SmaInverterVersion


def get_default_config() -> dict:
    return {
        "name": "SMA ModbusTCP Wechselrichter",
        "id": 0,
        "type": "inverter_modbus_tcp",
        "configuration": {
            "version": SmaInverterVersion.default.value
        }
    }


log = logging.getLogger(__name__)


class SmaModbusTcpInverter:

    SMA_INT32_NAN = -0x80000000  # SMA uses this value to represent NaN

    def __init__(self, device_id: int, device_address: str, component_config: dict) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = modbus.ModbusClient(device_address)
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        self.__store.set(self.read_inverter_state())

    def read_inverter_state(self) -> InverterState:
        with self.__tcp_client:
            if self.component_config["configuration"]["version"] == SmaInverterVersion.default:
                # AC Wirkleistung über alle Phasen (W) [Pac]
                power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=3)
                # Gesamtertrag (Wh) [E-Total]
                energy = self.__tcp_client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)
            elif self.component_config["configuration"]["version"] == SmaInverterVersion.core2:
                # AC Wirkleistung über alle Phasen (W) [Pac]
                power = self.__tcp_client.read_holding_registers(40084, ModbusDataType.INT_16, unit=1) * 10
                # Gesamtertrag (Wh) [E-Total] SF=2!
                energy = self.__tcp_client.read_holding_registers(40094, ModbusDataType.UINT_32, unit=1) * 100
            else:
                raise FaultState.error("Unbekannte Version: "+str(self.component_config["configuration"]["version"]))

            if power == self.SMA_INT32_NAN:
                power = 0

            return InverterState(
                power=-max(power, 0),
                exported=energy
            )
