from typing import Optional
from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup


@auto_str
class YoulessConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


@auto_str
class Youless:
    def __init__(self,
                 name: str = "Youless",
                 type: str = "youless",
                 id: int = 0,
                 configuration: YoulessConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or YoulessConfiguration()


@auto_str
class YoulessInverterConfiguration:
    def __init__(self, source_s0: bool = True):
        self.source_s0 = source_s0


@auto_str
class YoulessInverterSetup(ComponentSetup[YoulessInverterConfiguration]):
    def __init__(self,
                 name: str = "Youless LS120 Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: YoulessInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or YoulessInverterConfiguration())
