from typing import Optional


class SaxpowerConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Saxpower:
    def __init__(self,
                 name: str = "Saxpower",
                 type: str = "saxpower",
                 id: int = 0,
                 configuration: SaxpowerConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SaxpowerConfiguration()


class SaxpowerBatConfiguration:
    def __init__(self):
        pass


class SaxpowerBatSetup:
    def __init__(self,
                 name: str = "Saxpower Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SaxpowerBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SaxpowerBatConfiguration()
