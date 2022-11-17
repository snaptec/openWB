from typing import Optional

from modules.common.component_setup import ComponentSetup


class DiscovergyConfiguration:
    def __init__(self, user: Optional[str] = None, password: Optional[str] = None):
        self.user = user
        self.password = password


class Discovergy:
    def __init__(self,
                 name: str = "Discovergy",
                 type: str = "discovergy",
                 id: int = 0,
                 configuration: DiscovergyConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or DiscovergyConfiguration()


class DiscovergyCounterConfiguration:
    def __init__(self, meter_id: Optional[str] = None):
        self.meter_id = meter_id


class DiscovergyCounterSetup:
    def __init__(self,
                 name: str = "Discovergy Zähler",
                 type: str = "counter",
                 id: Optional[int] = 0,
                 configuration: DiscovergyCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or DiscovergyCounterConfiguration()


class DiscovergyInverterConfiguration:
    def __init__(self, meter_id: Optional[str] = None):
        self.meter_id = meter_id


class DiscovergyInverterSetup(ComponentSetup[DiscovergyInverterConfiguration]):
    def __init__(self,
                 name: str = "Discovergy Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: DiscovergyInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or DiscovergyInverterConfiguration())
