from typing import Optional


class SonnenBatterieConfiguration:
    def __init__(self, variant: int = 0, ip_address: Optional[str] = None):
        self.variant = variant
        self.ip_address = ip_address


class SonnenBatterie:
    def __init__(self,
                 name: str = "SonnenBatterie",
                 type: str = "sonnenbatterie",
                 id: int = 0,
                 configuration: SonnenBatterieConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SonnenBatterieConfiguration()


class SonnenbatterieBatConfiguration:
    def __init__(self):
        pass


class SonnenbatterieBatSetup:
    def __init__(self,
                 name: str = "SonnenBatterie Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SonnenbatterieBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SonnenbatterieBatConfiguration()


class SonnenbatterieCounterConfiguration:
    def __init__(self):
        pass


class SonnenbatterieCounterSetup:
    def __init__(self,
                 name: str = "SonnenBatterie Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SonnenbatterieCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SonnenbatterieCounterConfiguration()


class SonnenbatterieInverterConfiguration:
    def __init__(self):
        pass


class SonnenbatterieInverterSetup:
    def __init__(self,
                 name: str = "SonnenBatterie Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SonnenbatterieInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SonnenbatterieInverterConfiguration()
