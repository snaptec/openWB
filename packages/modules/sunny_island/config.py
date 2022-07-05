from typing import Optional


class SunnyIslandConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SunnyIsland:
    def __init__(self,
                 name: str = "Sunny Island",
                 type: str = "sunny_island",
                 id: int = 0,
                 configuration: SunnyIslandConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SunnyIslandConfiguration()


class SunnyIslandBatConfiguration:
    def __init__(self):
        pass


class SunnyIslandBatSetup:
    def __init__(self,
                 name: str = "Sunny Island Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SunnyIslandBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SunnyIslandBatConfiguration()
