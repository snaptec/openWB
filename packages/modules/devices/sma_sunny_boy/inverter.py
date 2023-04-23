#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.devices.sma_sunny_boy.config import SmaSunnyBoyInverterSetup
from modules.devices.sma_sunny_boy.inv_version import SmaInverterVersion

log = logging.getLogger(__name__)


class SmaSunnyBoyInverter:

    SMA_INT32_NAN = -0x80000000  # SMA uses this value to represent NaN

    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SmaSunnyBoyInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SmaSunnyBoyInverterSetup, component_config)
        self.tcp_client = tcp_client
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        self.store.set(self.read())

    def read(self) -> InverterState:
        if self.component_config.configuration.version == SmaInverterVersion.default:
            # AC Wirkleistung über alle Phasen (W) [Pac]
            power_total = self.tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=3)
            # Gesamtertrag (Wh) [E-Total]
            energy = self.tcp_client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)
            # Bei Hybrid Wechselrichtern treten Abweichungen auf, die in der Nacht
            # immer wieder Generatorleistung anzeigen (0-50 Watt). Um dies zu verhindern, schauen wir uns
            # zunächst an, ob vom DC Teil überhaupt Leistung kommt. Ist dies nicht der Fall, können wir power
            # gleich auf 0 setzen.
            # Leistung DC an Eingang 1 und 2
            dc_power = (self.tcp_client.read_holding_registers(30773, ModbusDataType.INT_32, unit=3) +
                        self.tcp_client.read_holding_registers(30961, ModbusDataType.INT_32, unit=3))
        elif self.component_config.configuration.version == SmaInverterVersion.core2:
            # AC Wirkleistung über alle Phasen (W) [Pac]
            power_total = self.tcp_client.read_holding_registers(40084, ModbusDataType.INT_16, unit=1) * 10
            # Gesamtertrag (Wh) [E-Total] SF=2!
            energy = self.tcp_client.read_holding_registers(40094, ModbusDataType.UINT_32, unit=1) * 100
            dc_power = self.tcp_client.read_holding_registers(40101, ModbusDataType.UINT_32, unit=1) * 100
        elif self.component_config.configuration.version == SmaInverterVersion.datamanager:
            # AC Wirkleistung über alle Phasen (W) [Pac]
            power_total = self.tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=2)
            # Total eingespeiste Energie auf allen Außenleitern (Wh) [E-Total]
            energy = self.tcp_client.read_holding_registers(30513, ModbusDataType.UINT_64, unit=2)
            # DC-Power = power_total - Cluster-Controller gibt in Register 30775 immer korrekte Werte aus,
            # daher ist wie bei SmaInverterVersion.default keine Prüfung auf DC-Leistung notwendig.
            # Aus kompatibilitätsgründen wird dc_power auf den Wert der AC-Wirkleistung gesetzt.
            dc_power = power_total
        else:
            raise FaultState.error("Unbekannte Version "+str(self.component_config.configuration.version))
        if power_total == self.SMA_INT32_NAN:
            power_total = 0

        inverter_state = InverterState(
            power=power_total * -1,
            dc_power=dc_power * -1,
            exported=energy
        )
        log.debug("WR {}: {}".format(self.tcp_client.address, inverter_state))
        return inverter_state


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyBoyInverterSetup)
