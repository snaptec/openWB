from typing import Optional


class SungrowConfiguration:
    def __init__(self, ip_address: Optional[str] = None, port: int = 502):
        self.ip_address = ip_address
        self.port = port


class Sungrow:
    def __init__(self,
                 name: str = "Sungrow",
                 type: str = "sungrow",
                 id: int = 0,
                 configuration: SungrowConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SungrowConfiguration()


class SungrowBatConfiguration:
    def __init__(self, id: int = 1):
        self.id = id


class SungrowBatSetup:
    def __init__(self,
                 name: str = "Sungrow Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SungrowBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SungrowBatConfiguration()


class SungrowCounterConfiguration:
    def __init__(self, version=1, id: int = 1):
        self.version = version
        self.id = id


class SungrowCounterSetup:
    def __init__(self,
                 name: str = "Sungrow Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SungrowCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SungrowCounterConfiguration()


class SungrowInverterConfiguration:
    def __init__(self, id: int = 1):
        self.id = id


class SungrowInverterSetup:
    def __init__(self,
                 name: str = "Sungrow Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SungrowInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SungrowInverterConfiguration()
