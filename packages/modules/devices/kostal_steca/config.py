from typing import Optional
from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup


@auto_str
class KostalStecaConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


@auto_str
class KostalSteca:
    def __init__(self,
                 name: str = "Kostal Piko MP oder Steca Grid Coolcept",
                 type: str = "kostal_steca",
                 id: int = 0,
                 configuration: KostalStecaConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalStecaConfiguration()


@auto_str
class KostalStecaInverterConfiguration:
    def __init__(self, variant_steca: bool = True):
        self.variant_steca = variant_steca


@auto_str
class KostalStecaInverterSetup(ComponentSetup[KostalStecaInverterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Piko MP oder Steca Grid Coolcept Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: KostalStecaInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalStecaInverterConfiguration())
