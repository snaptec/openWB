from typing import Optional

from modules.common.component_setup import ComponentSetup


class KostalPikoConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class KostalPiko:
    def __init__(self,
                 name: str = "Kostal Piko",
                 type: str = "kostal_piko",
                 id: int = 0,
                 configuration: KostalPikoConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalPikoConfiguration()


class KostalPikoCounterConfiguration:
    def __init__(self):
        pass


class KostalPikoCounterSetup(ComponentSetup[KostalPikoCounterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Piko Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: KostalPikoCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPikoCounterConfiguration())


class KostalPikoInverterConfiguration:
    def __init__(self, bat_configured: bool = False):
        self.bat_configured = bat_configured


class KostalPikoInverterSetup(ComponentSetup[KostalPikoInverterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Piko Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: KostalPikoInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPikoInverterConfiguration())
