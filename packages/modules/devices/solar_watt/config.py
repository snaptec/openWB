from typing import Optional

from modules.common.component_setup import ComponentSetup


class SolarWattConfiguration:
    def __init__(self, ip_address: Optional[str] = None, energy_manager: bool = True):
        self.ip_adress = ip_address
        self.energy_manager = energy_manager


class SolarWatt:
    def __init__(self,
                 name: str = "Solarwatt/My Reserve",
                 type: str = "solar_watt",
                 id: int = 0,
                 configuration: SolarWattConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolarWattConfiguration()


class SolarWattBatConfiguration:
    def __init__(self):
        pass


class SolarWattBatSetup(ComponentSetup[SolarWattBatConfiguration]):
    def __init__(self,
                 name: str = "Solarwatt/My Reserve Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SolarWattBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarWattBatConfiguration())


class SolarWattCounterConfiguration:
    def __init__(self):
        pass


class SolarWattCounterSetup(ComponentSetup[SolarWattCounterConfiguration]):
    def __init__(self,
                 name: str = "Solarwatt/My Reserve Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolarWattCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarWattCounterConfiguration())


class SolarWattInverterConfiguration:
    def __init__(self):
        pass


class SolarWattInverterSetup(ComponentSetup[SolarWattInverterConfiguration]):
    def __init__(self,
                 name: str = "Solarwatt/My Reserve Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolarWattInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolarWattInverterConfiguration())
