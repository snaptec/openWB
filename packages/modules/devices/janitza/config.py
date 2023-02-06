from typing import Optional

from modules.common.component_setup import ComponentSetup


class JanitzaConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Janitza:
    def __init__(self,
                 name: str = "Janitza",
                 type: str = "janitza",
                 id: int = 0,
                 configuration: JanitzaConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or JanitzaConfiguration()


class JanitzaCounterConfiguration:
    def __init__(self):
        pass


class JanitzaCounterSetup(ComponentSetup[JanitzaCounterConfiguration]):
    def __init__(self,
                 name: str = "Janitza Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: JanitzaCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or JanitzaCounterConfiguration())
