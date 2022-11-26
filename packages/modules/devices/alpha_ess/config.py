from typing import Optional

from modules.common.component_setup import ComponentSetup


class AlphaEssConfiguration:
    def __init__(self, source: int = 0, ip_address: Optional[str] = None, version: int = 1):
        self.source = source  # 0: AlphaEss-Kit, 1: Hi5/10 mit variabler IP
        self.ip_address = ip_address
        self.version = version  # 0: <V1.23, 1: >= V1.23


class AlphaEss:
    def __init__(self,
                 name: str = "Alpha ESS",
                 type: str = "alpha_ess",
                 id: int = 0,
                 configuration: AlphaEssConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or AlphaEssConfiguration()


class AlphaEssBatConfiguration:
    def __init__(self):
        pass


class AlphaEssBatSetup(ComponentSetup[AlphaEssBatConfiguration]):
    def __init__(self,
                 name: str = "Alpha ESS Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: AlphaEssBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or AlphaEssBatConfiguration())


class AlphaEssCounterConfiguration:
    def __init__(self):
        pass


class AlphaEssCounterSetup(ComponentSetup[AlphaEssCounterConfiguration]):
    def __init__(self,
                 name: str = "Alpha ESS Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: AlphaEssCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or AlphaEssCounterConfiguration())


class AlphaEssInverterConfiguration:
    def __init__(self):
        pass


class AlphaEssInverterSetup(ComponentSetup[AlphaEssInverterConfiguration]):
    def __init__(self,
                 name: str = "Alpha ESS Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: AlphaEssInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or AlphaEssInverterConfiguration())
