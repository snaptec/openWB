from typing import Optional

from modules.common.component_setup import ComponentSetup


class KostalSemConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class KostalSem:
    def __init__(self,
                 name: str = "Kostal Smart Energy Meter oder TQ EM 410",
                 type: str = "kostal_sem",
                 id: int = 0,
                 configuration: KostalSemConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalSemConfiguration()


class KostalSemCounterConfiguration:
    def __init__(self, meter_id: Optional[str] = None):
        self.meter_id = meter_id


class KostalSemCounterSetup(ComponentSetup[KostalSemCounterConfiguration]):
    def __init__(self,
                 name: str = "Kostal Smart Energy Meter oder TQ EM 410 Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: KostalSemCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalSemCounterConfiguration()
