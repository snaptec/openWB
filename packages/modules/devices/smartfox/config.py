from typing import Optional

from modules.common.component_setup import ComponentSetup


class SmartfoxConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Smartfox:
    def __init__(self,
                 name: str = "Smartfox",
                 type: str = "smartfox",
                 id: int = 0,
                 configuration: SmartfoxConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmartfoxConfiguration()


class SmartfoxCounterConfiguration:
    def __init__(self):
        pass


class SmartfoxCounterSetup(ComponentSetup[SmartfoxCounterConfiguration]):
    def __init__(self,
                 name: str = "Smartfox Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmartfoxCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmartfoxCounterConfiguration())
