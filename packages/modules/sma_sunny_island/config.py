from typing import Optional

from modules.common.component_setup import ComponentSetup


class SmaSunnyIslandConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SmaSunnyIsland:
    def __init__(self,
                 name: str = "SMA Sunny Island",
                 type: str = "sma_sunny_island",
                 id: int = 0,
                 configuration: SmaSunnyIslandConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaSunnyIslandConfiguration()


class SmaSunnyIslandBatConfiguration:
    def __init__(self):
        pass


class SmaSunnyIslandBatSetup(ComponentSetup[SmaSunnyIslandBatConfiguration]):
    def __init__(self,
                 name: str = "SMA Sunny Island Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SmaSunnyIslandBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaSunnyIslandBatConfiguration())
