from typing import Optional

from modules.common.component_setup import ComponentSetup


class SolarLogConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class SolarLog:
    def __init__(self,
                 name: str = "Solar-Log",
                 type: str = "solar_log",
                 id: int = 0,
                 configuration: SolarLogConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolarLogConfiguration()


class SolarLogCounterConfiguration:
    def __init__(self):
        pass


class SolarLogCounterSetup(ComponentSetup[SolarLogCounterConfiguration]):
    def __init__(self,
                 name: str = "Solar-Log Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolarLogCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarLogCounterConfiguration())


class SolarLogInverterConfiguration:
    def __init__(self):
        pass


class SolarLogInverterSetup(ComponentSetup[SolarLogInverterConfiguration]):
    def __init__(self,
                 name: str = "Solar-Log Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolarLogInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarLogInverterConfiguration())
