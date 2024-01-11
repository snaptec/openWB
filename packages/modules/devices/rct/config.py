from typing import Optional
from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup


@auto_str
class RctConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


@auto_str
class Rct:
    def __init__(self,
                 name: str = "RCT",
                 type: str = "rct",
                 id: int = 0,
                 configuration: RctConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or RctConfiguration()


@auto_str
class RctBatConfiguration:
    def __init__(self):
        pass


@auto_str
class RctBatSetup(ComponentSetup[RctBatConfiguration]):
    def __init__(self,
                 name: str = "RCT Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: RctBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or RctBatConfiguration())


@auto_str
class RctCounterConfiguration:
    def __init__(self):
        pass


@auto_str
class RctCounterSetup(ComponentSetup[RctCounterConfiguration]):
    def __init__(self,
                 name: str = "RCT Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: RctCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or RctCounterConfiguration())


@auto_str
class RctInverterConfiguration:
    def __init__(self):
        pass


@auto_str
class RctInverterSetup(ComponentSetup[RctInverterConfiguration]):
    def __init__(self,
                 name: str = "RCT Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: RctInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or RctInverterConfiguration())
