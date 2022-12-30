from typing import Optional

from modules.common.component_setup import ComponentSetup


class SiemensSentronConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SiemensSentron:
    def __init__(self,
                 name: str = "Siemens Sentron",
                 type: str = "siemens_sentron",
                 id: int = 0,
                 configuration: SiemensSentronConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensSentronConfiguration()


class SiemensSentronCounterConfiguration:
    def __init__(self):
        pass


class SiemensSentronCounterSetup(ComponentSetup[SiemensSentronCounterConfiguration]):
    def __init__(self,
                 name: str = "Siemens Sentron Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SiemensSentronCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SiemensSentronCounterConfiguration())
