from typing import Optional

from modules.sma_sunny_boy.inverter_version import SmaInverterVersion


class SmaSunnyBoyConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SmaSunnyBoy:
    def __init__(self,
                 name: str = "Sma Sunny Boy",
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


class SmaSunnyBoyBatSetup:
    def __init__(self,
                 name: str = "Sma Sunny Boy Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SmaSunnyBoyBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyBoyBatConfiguration()


class SmaSunnyBoySmartEnergyBatConfiguration:
    def __init__(self):
        pass


class SmaSunnyBoySmartEnergyBatSetup:
    def __init__(self,
                 name: str = "Sma Sunny Boy Smart Energy Speicher",
                 type: str = "bat_smart_energy",
                 id: int = 0,
                 configuration: SmaSunnyBoySmartEnergyBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyBoySmartEnergyBatConfiguration()


class SmaSunnyBoyCounterConfiguration:
    def __init__(self):
        pass


class SmaSunnyBoyCounterSetup:
    def __init__(self,
                 name: str = "Sma Sunny Boy Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmaSunnyBoyCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyBoyCounterConfiguration()


class SmaSunnyBoyInverterConfiguration:
    def __init__(self, hybrid: bool = False, version: SmaInverterVersion = SmaInverterVersion.default):
        self.hybrid = hybrid
        self.version = version


class SmaSunnyBoyInverterSetup:
    def __init__(self,
                 name: str = "Sma Sunny Boy/Tripower Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmaSunnyBoyInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyBoyInverterConfiguration()
