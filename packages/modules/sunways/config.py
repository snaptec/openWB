from typing import Optional

from modules.common.component_setup import ComponentSetup


class SunwaysConfiguration:
    def __init__(self, password: Optional[str] = None, ip_address: Optional[str] = None):
        self.password = password
        self.ip_address = ip_address


class Sunways:
    def __init__(self,
                 name: str = "Sunways",
                 type: str = "sunways",
                 id: int = 0,
                 configuration: SunwaysConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SunwaysConfiguration()


class SunwaysInverterConfiguration:
    def __init__(self):
        pass


class SunwaysInverterSetup(ComponentSetup[SunwaysInverterConfiguration]):
    def __init__(self,
                 name: str = "Sunways Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SunwaysInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SunwaysInverterConfiguration())
