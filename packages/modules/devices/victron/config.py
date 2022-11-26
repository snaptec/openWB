from typing import Optional

from modules.common.component_setup import ComponentSetup


class VictronConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Victron:
    def __init__(self,
                 name: str = "Victron",
                 type: str = "victron",
                 id: int = 0,
                 configuration: VictronConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or VictronConfiguration()


class VictronBatConfiguration:
    def __init__(self, modbus_id: int = 100):
        self.modbus_id = modbus_id


class VictronBatSetup(ComponentSetup[VictronBatConfiguration]):
    def __init__(self,
                 name: str = "Victron Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: VictronBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VictronBatConfiguration())


class VictronCounterConfiguration:
    def __init__(self, energy_meter: bool = True, modbus_id: int = 1):
        self.energy_meter = energy_meter
        self.modbus_id = modbus_id


class VictronCounterSetup(ComponentSetup[VictronCounterConfiguration]):
    def __init__(self,
                 name: str = "Victron Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: VictronCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VictronCounterConfiguration())


class VictronInverterConfiguration:
    def __init__(self, mppt: bool = False, modbus_id: int = 100):
        self.mppt = mppt
        self.modbus_id = modbus_id


class VictronInverterSetup(ComponentSetup[VictronInverterConfiguration]):
    def __init__(self,
                 name: str = "Victron Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: VictronInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VictronInverterConfiguration())
