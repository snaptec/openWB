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
            "version": SmaInverterVersion.default.value,
            "hybrid": False
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
                power_total = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=3)
                # Gesamtertrag (Wh) [E-Total]
                energy = self.__tcp_client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)
            elif self.component_config["configuration"]["version"] == SmaInverterVersion.core2:
                # AC Wirkleistung über alle Phasen (W) [Pac]
                power_total = self.__tcp_client.read_holding_registers(40084, ModbusDataType.INT_16, unit=1) * 10
                # Gesamtertrag (Wh) [E-Total] SF=2!
                energy = self.__tcp_client.read_holding_registers(40094, ModbusDataType.UINT_32, unit=1) * 100
            else:
                raise FaultState.error("Unbekannte Version "+str(self.component_config["configuration"]["version"]))
            if self.component_config["configuration"]["hybrid"] is True:
                if power_total != self.SMA_INT32_NAN:
                    # Bei Hybrid Wechselrichtern muss man hier die Batterie Lade- und Entladeleistung abziehen, um auf
                    # die echte Generator Leistung zu kommen. Leider treten hierbei Abweichungen auf, die in der Nacht
                    # immer wieder Generatorleistung anzeigen (0-50 Watt). Um dies zu verhindern, schauen wir uns
                    # zunächst an, ob vom DC Teil überhaupt Leistung kommt. Ist dies nicht der Fall, können wir power
                    # gleich auf 0 setzen. Ansonsten rechnen wir die Batterieladung raus.
                    # Leistung DC an Eingang 1
                    dc_power = self.__tcp_client.read_holding_registers(30773, ModbusDataType.INT_32, unit=3)
                    if dc_power == 0:
                        # Wenn wir an DC Eingang 1 keine Leistung haben müssen wir noch den DC Eingang 2 prüfen
                        dc_power = self.__tcp_client.read_holding_registers(30961, ModbusDataType.INT_32, unit=3)
                    if dc_power == 0:
                        power_total = 0
                    else:
                        battery_discharge_power = self.__tcp_client.read_holding_registers(
                            31395, ModbusDataType.UINT_32, unit=3)
                        power_total -= battery_discharge_power
                        battery_charge_power = self.__tcp_client.read_holding_registers(
                            31393, ModbusDataType.UINT_32, unit=3)
                        power_total += battery_charge_power

                # Gesamtertrag (Wh) [E-Total]
                energy = self.__tcp_client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)
                # Batterieentladung (Wh) (Diese hat einen negativen Einfluss auf die Gesamtenergie)
                battery_discharge_energy = self.__tcp_client.read_holding_registers(
                    31401, ModbusDataType.UINT_64, unit=3)
                energy -= battery_discharge_energy
                # Batterieladung (Wh) (Diese hat einen positiven Einfluss auf die Gesamtenergie)
                battery_charge_enegery = self.__tcp_client.read_holding_registers(31397, ModbusDataType.UINT_64, unit=3)
                energy += battery_charge_enegery

            if power_total == self.SMA_INT32_NAN:
                power_total = 0

            return InverterState(
                power=-max(power_total, 0),
                exported=energy
            )
