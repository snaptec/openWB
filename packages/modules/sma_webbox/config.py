from typing import Optional

from modules.common.component_setup import ComponentSetup


class SmaWWebboxConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SmaWebbox:
    def __init__(self,
                 name: str = "SMA Webbox",
                 type: str = "sma_webbox",
                 id: int = 0,
                 configuration: SmaWWebboxConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaWWebboxConfiguration()


class SmaWebboxInverterConfiguration:
    def __init__(self):
        pass


class SmaWebboxInverterSetup(ComponentSetup[SmaWebboxInverterConfiguration]):
    def __init__(self,
                 name: str = "SMA Wechselrichter Webbox",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmaWebboxInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaWebboxInverterConfiguration())
