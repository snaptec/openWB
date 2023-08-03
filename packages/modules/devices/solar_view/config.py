from typing import Optional

from modules.common.component_setup import ComponentSetup


class SolarViewConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 port: Optional[int] = None,
                 timeout: int = 3):
        self.ip_address = ip_address
        self.port = port  # Wertebereich [1, 65535]
        self.timeout = timeout


class SolarView:
    def __init__(self,
                 name: str = "SolarView",
                 type: str = "solar_view",
                 id: int = 0,
                 configuration: SolarViewConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolarViewConfiguration()


class SolarViewCounterConfiguration:
    def __init__(self):
        pass


class SolarViewCounterSetup(ComponentSetup[SolarViewCounterConfiguration]):
    def __init__(self,
                 name: str = "SolarView Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolarViewCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarViewCounterConfiguration())


class SolarViewInverterConfiguration:
    def __init__(self, command: Optional[str] = None):
        self.command = command


class SolarViewInverterSetup(ComponentSetup[SolarViewInverterConfiguration]):
    def __init__(self,
                 name: str = "SolarView Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolarViewInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarViewInverterConfiguration())
