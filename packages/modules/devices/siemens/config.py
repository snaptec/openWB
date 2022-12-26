from typing import Optional

from modules.common.component_setup import ComponentSetup


class SiemensConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Siemens:
    def __init__(self,
                 name: str = "Siemens",
                 type: str = "siemens",
                 id: int = 0,
                 configuration: SiemensConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SiemensConfiguration()


class SiemensBatConfiguration:
    def __init__(self):
        pass


class SiemensBatSetup(ComponentSetup[SiemensBatConfiguration]):
    def __init__(self,
                 name: str = "Siemens Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SiemensBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SiemensBatConfiguration())


class SiemensCounterConfiguration:
    def __init__(self):
        pass


class SiemensCounterSetup(ComponentSetup[SiemensCounterConfiguration]):
    def __init__(self,
                 name: str = "Siemens Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SiemensCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SiemensCounterConfiguration())


class SiemensInverterConfiguration:
    def __init__(self):
        pass


class SiemensInverterSetup(ComponentSetup[SiemensInverterConfiguration]):
    def __init__(self,
                 name: str = "Siemens Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SiemensInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SiemensInverterConfiguration())
