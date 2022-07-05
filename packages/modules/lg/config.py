from typing import Optional


class LgConfiguration:
    def __init__(self, ip_address: Optional[str] = None, password: Optional[str] = None):
        self.ip_address = ip_address
        self.password = password


class LG:
    def __init__(self,
                 name: str = "LG ESS V1.0",
                 type: str = "lg",
                 id: int = 0,
                 configuration: LgConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or LgConfiguration()


class LgBatConfiguration:
    def __init__(self):
        pass


class LgBatSetup:
    def __init__(self,
                 name: str = "LG ESS V1.0 Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: LgBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or LgBatConfiguration()


class LgCounterConfiguration:
    def __init__(self):
        pass


class LgCounterSetup:
    def __init__(self,
                 name: str = "LG ESS V1.0 Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: LgCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or LgCounterConfiguration()


class LgInverterConfiguration:
    def __init__(self):
        pass


class LgInverterSetup:
    def __init__(self,
                 name: str = "LG ESS V1.0 Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: LgInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or LgInverterConfiguration()
