from typing import Optional


class SiemensConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Siemens:
    def __init__(self,
                 name: str = "Siemens",
                 type: str = "siemens",
                 id: int = 0,
                 configuration: SiemensConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensConfiguration()


class SiemensBatConfiguration:
    def __init__(self):
        pass


class SiemensBatSetup:
    def __init__(self,
                 name: str = "Siemens Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SiemensBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensBatConfiguration()


class SiemensCounterConfiguration:
    def __init__(self):
        pass


class SiemensCounterSetup:
    def __init__(self,
                 name: str = "Siemens Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SiemensCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensCounterConfiguration()


class SiemensInverterConfiguration:
    def __init__(self):
        pass


class SiemensInverterSetup:
    def __init__(self,
                 name: str = "Siemens Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SiemensInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensInverterConfiguration()
