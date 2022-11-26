from typing import Optional

from modules.common.component_setup import ComponentSetup
from modules.devices.sma_sunny_boy.inv_version import SmaInverterVersion


class SmaSunnyBoyConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SmaSunnyBoy:
    def __init__(self,
                 name: str = "SMA Sunny Boy",
                 type: str = "sma_sunny_boy",
                 id: int = 0,
                 configuration: SmaSunnyBoyConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyBoyConfiguration()


class SmaSunnyBoyBatConfiguration:
    def __init__(self):
        pass


class SmaSunnyBoyBatSetup(ComponentSetup[SmaSunnyBoyBatConfiguration]):
    def __init__(self,
                 name: str = "Sma Sunny Boy Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SmaSunnyBoyBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaSunnyBoyBatConfiguration())


class SmaSunnyBoySmartEnergyBatConfiguration:
    def __init__(self):
        pass


class SmaSunnyBoySmartEnergyBatSetup(ComponentSetup[SmaSunnyBoySmartEnergyBatConfiguration]):
    def __init__(self,
                 name: str = "Sma Sunny Boy Smart Energy Speicher",
                 type: str = "bat_smart_energy",
                 id: int = 0,
                 configuration: SmaSunnyBoySmartEnergyBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaSunnyBoySmartEnergyBatConfiguration())


class SmaSunnyBoyCounterConfiguration:
    def __init__(self):
        pass


class SmaSunnyBoyCounterSetup(ComponentSetup[SmaSunnyBoyCounterConfiguration]):
    def __init__(self,
                 name: str = "Sma Sunny Boy Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmaSunnyBoyCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaSunnyBoyCounterConfiguration())


class SmaSunnyBoyInverterConfiguration:
    def __init__(self, hybrid: bool = False, version: SmaInverterVersion = SmaInverterVersion.default):
        self.hybrid = hybrid
        self.version = version


class SmaSunnyBoyInverterSetup(ComponentSetup[SmaSunnyBoyInverterConfiguration]):
    def __init__(self,
                 name: str = "Sma Sunny Boy/Tripower Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmaSunnyBoyInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaSunnyBoyInverterConfiguration())
