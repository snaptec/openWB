from typing import Optional

from modules.common.component_setup import ComponentSetup


class PowerfoxConfiguration:
    def __init__(self, user: Optional[str] = None, password: Optional[str] = None):
        self.user = user
        self.password = password


class Powerfox:
    def __init__(self,
                 name: str = "Powerfox",
                 type: str = "powerfox",
                 id: int = 0,
                 configuration: PowerfoxConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PowerfoxConfiguration()


class PowerfoxCounterConfiguration:
    def __init__(self, id: str):
        self.id = id


class PowerfoxCounterSetup(ComponentSetup[PowerfoxCounterConfiguration]):
    def __init__(self,
                 name: str = "Powerfox Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: PowerfoxCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or PowerfoxCounterConfiguration())


class PowerfoxInverterConfiguration:
    def __init__(self, id: str):
        self.id = id


class PowerfoxInverterSetup(ComponentSetup[PowerfoxInverterConfiguration]):
    def __init__(self,
                 name: str = "Powerfox Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: PowerfoxInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or PowerfoxInverterConfiguration())
