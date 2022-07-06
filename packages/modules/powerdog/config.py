from typing import Optional


class PowerdogConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Powerdog:
    def __init__(self,
                 name: str = "Powerdog",
                 type: str = "powerdog",
                 id: int = 0,
                 configuration: PowerdogConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PowerdogConfiguration()


class PowerdogCounterConfiguration:
    def __init__(self):
        pass


class PowerdogCounterSetup:
    def __init__(self,
                 name: str = "Powerdog Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: PowerdogCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PowerdogCounterConfiguration()


class PowerdogInverterConfiguration:
    def __init__(self):
        pass


class PowerdogInverterSetup:
    def __init__(self,
                 name: str = "Powerdog Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: PowerdogInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PowerdogInverterConfiguration()
