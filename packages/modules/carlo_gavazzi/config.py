from typing import Optional

from modules.common.component_setup import ComponentSetup


class CarloGavazziConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class CarloGavazzi:
    def __init__(self,
                 name: str = "Carlo Gavazzi",
                 type: str = "carlo_gavazzi",
                 id: int = 0,
                 configuration: CarloGavazziConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or CarloGavazziConfiguration()


class CarloGavazziCounterConfiguration:
    def __init__(self):
        pass


class CarloGavazziCounterSetup(ComponentSetup[CarloGavazziCounterConfiguration]):
    def __init__(self,
                 name: str = "Carlo Gavazzi Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: CarloGavazziCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or CarloGavazziCounterConfiguration())
