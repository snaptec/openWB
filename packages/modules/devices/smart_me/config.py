from typing import Optional

from modules.common.component_setup import ComponentSetup


class SmartMeConfiguration:
    def __init__(self, user: Optional[str] = None, password: Optional[str] = None):
        self.user = user
        self.password = password


class SmartMe:
    def __init__(self,
                 name: str = "smart-me",
                 type: str = "smart_me",
                 id: int = 0,
                 configuration: SmartMeConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmartMeConfiguration()


class SmartMeCounterConfiguration:
    def __init__(self, id: Optional[str] = None):
        self.id = id


class SmartMeCounterSetup(ComponentSetup[SmartMeCounterConfiguration]):
    def __init__(self,
                 name: str = "smart-me Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmartMeCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmartMeCounterConfiguration())


class SmartMeInverterConfiguration:
    def __init__(self, id: Optional[str] = None):
        self.id = id


class SmartMeInverterSetup(ComponentSetup[SmartMeInverterConfiguration]):
    def __init__(self,
                 name: str = "smart-me Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmartMeInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmartMeInverterConfiguration())
