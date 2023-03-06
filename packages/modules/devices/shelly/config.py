from modules.common.component_setup import ComponentSetup
from typing import Optional
from helpermodules.auto_str import auto_str


@auto_str
class ShellyConfiguration:
    def __init__(self, address: str = None, generation: Optional[int] = None):
        self.address = address
        self.generation = generation


@auto_str
class Shelly:
    def __init__(self,
                 name: str = "Shelly",
                 type: str = "shelly",
                 id: int = 0,
                 configuration: ShellyConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or ShellyConfiguration()


@auto_str
class ShellyInverterConfiguration:
    def __init__(self) -> None:
        pass


@auto_str
class ShellyInverterSetup(ComponentSetup[ShellyInverterConfiguration]):
    def __init__(self,
                 name: str = "Shelly Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: ShellyInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or ShellyInverterConfiguration())
