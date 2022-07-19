from typing import Optional


class GoodWeConfiguration:
    def __init__(self, ip_address: Optional[str] = None, id: int = 247):
        self.ip_address = ip_address
        self.id = id


class GoodWe:
    def __init__(self,
                 name: str = "GoodWe",
                 type: str = "good_we",
                 id: int = 0,
                 configuration: GoodWeConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or GoodWeConfiguration()


class GoodWeBatConfiguration:
    def __init__(self):
        pass


class GoodWeBatSetup:
    def __init__(self,
                 name: str = "GoodWe Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: GoodWeBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or GoodWeBatConfiguration()


class GoodWeCounterConfiguration:
    def __init__(self):
        pass


class GoodWeCounterSetup:
    def __init__(self,
                 name: str = "GoodWe Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: GoodWeCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or GoodWeCounterConfiguration()


class GoodWeInverterConfiguration:
    def __init__(self):
        pass


class GoodWeInverterSetup:
    def __init__(self,
                 name: str = "GoodWe Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: GoodWeInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or GoodWeInverterConfiguration()
