from typing import Optional


class BatterXConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class BatterX:
    def __init__(self,
                 name: str = "BatterX",
                 type: str = "batterx",
                 id: int = 0,
                 configuration: BatterXConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatterXConfiguration()


class BatterXBatConfiguration:
    def __init__(self):
        pass


class BatterXBatSetup:
    def __init__(self,
                 name: str = "BatterX Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BatterXBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatterXBatConfiguration()


class BatterXCounterConfiguration:
    def __init__(self):
        pass


class BatterXCounterSetup:
    def __init__(self,
                 name: str = "BatterX Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: BatterXCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatterXCounterConfiguration()


class BatterXInverterConfiguration:
    def __init__(self):
        pass


class BatterXInverterSetup:
    def __init__(self,
                 name: str = "BatterX Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: BatterXInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatterXInverterConfiguration()
