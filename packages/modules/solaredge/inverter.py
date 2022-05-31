#!/usr/bin/env python3
import logging
import math

from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "SolarEdge Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "modbus_id": 1
        }
    }


UINT16_UNSUPPORTED = 0xFFFF


class SolaredgeInverter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, state: InverterState) -> None:
        self.__store.set(state)

    def read_state(self):
        unit = self.component_config["configuration"]["modbus_id"]
        with self.__tcp_client:
            # 40083 = AC Power value (Watt), 40084 = AC Power scale factor
            power_base, power_scale = self.__tcp_client.read_holding_registers(
                40083, [ModbusDataType.INT_16] * 2, unit=unit)
            # 40093 = AC Lifetime Energy production (Watt hours)
            energy_base, energy_scale = self.__tcp_client.read_holding_registers(
                40093, [ModbusDataType.UINT_32, ModbusDataType.INT_16], unit=unit
            )
            # 40072/40073/40074 = AC Phase A/B/C Current value (Amps)
            # 40075 = AC Current scale factor
            currents_base_scale = self.__tcp_client.read_holding_registers(
                40072, [ModbusDataType.UINT_16] * 3 + [ModbusDataType.INT_16], unit=unit
            )
        log.debug(
            "slave=%d: power=%d*10^%d, energy=%d*10^%d, currents=%s * 10^%d",
            unit, power_base, power_scale, energy_base, energy_scale, currents_base_scale[0:3], currents_base_scale[3]
        )
        # Registers that are not applicable to a meter class return the unsupported value. (e.g. Single Phase
        # meters will support only summary and phase A values):
        currents_scale = math.pow(10, currents_base_scale[3])
        currents = [0.0]*3
        for i in range(3):
            if currents_base_scale[i] == UINT16_UNSUPPORTED:
                currents_base_scale[i] = 0
            currents[i] = currents_base_scale[i] * currents_scale
        power = power_base * math.pow(10, power_scale) * -1
        exported = energy_base * math.pow(10, energy_scale)

        return InverterState(
            power=power,
            exported=exported,
            currents=currents
        )
