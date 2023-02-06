from typing import Optional

from modules.common.component_setup import ComponentSetup


class LgConfiguration:
    def __init__(self, ip_address: Optional[str] = None, password: Optional[str] = None):
        self.ip_address = ip_address
        self.password = password


class LG:
    def __init__(self,
                 name: str = "LG ESS V1.0",
                 type: str = "lg",
                 id: int = 0,
                 configuration: LgConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or LgConfiguration()


class LgBatConfiguration:
    def __init__(self):
        pass


class LgBatSetup(ComponentSetup[LgBatConfiguration]):
    def __init__(self,
                 name: str = "LG ESS V1.0 Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: LgBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or LgBatConfiguration())


class LgCounterConfiguration:
    def __init__(self):
        pass


class LgCounterSetup(ComponentSetup[LgCounterConfiguration]):
    def __init__(self,
                 name: str = "LG ESS V1.0 Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: LgCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or LgCounterConfiguration())


class LgInverterConfiguration:
    def __init__(self):
        pass


class LgInverterSetup(ComponentSetup[LgInverterConfiguration]):
    def __init__(self,
                 name: str = "LG ESS V1.0 Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: LgInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or LgInverterConfiguration())
