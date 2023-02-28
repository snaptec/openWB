from typing import Optional

from modules.common.component_setup import ComponentSetup


class KostalPlenticoreConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class KostalPlenticore:
    def __init__(self,
                 name: str = "Kostal Plenticore",
                 type: str = "kostal_plenticore",
                 id: int = 0,
                 configuration: KostalPlenticoreConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalPlenticoreConfiguration()


class KostalPlenticoreBatConfiguration:
    def __init__(self):
        pass


class KostalPlenticoreBatSetup(ComponentSetup[KostalPlenticoreBatConfiguration]):
    def __init__(self,
                 name: str = "Kostal Plenticore Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: KostalPlenticoreBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPlenticoreBatConfiguration())


class KostalPlenticoreCounterConfiguration:
    def __init__(self):
        pass


class KostalPlenticoreCounterSetup(ComponentSetup[KostalPlenticoreCounterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Plenticore Zähler",
                 type: str = "counter",
                 id: Optional[int] = 0,
                 configuration: KostalPlenticoreCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPlenticoreCounterConfiguration())


class KostalPlenticoreInverterConfiguration:
    def __init__(self):
        pass


class KostalPlenticoreInverterSetup(ComponentSetup[KostalPlenticoreInverterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Plenticore Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: KostalPlenticoreInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or KostalPlenticoreInverterConfiguration())
