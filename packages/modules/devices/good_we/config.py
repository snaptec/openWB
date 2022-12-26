from typing import Optional

from modules.common.component_setup import ComponentSetup


class GoodWeConfiguration:
    def __init__(self, ip_address: Optional[str] = None, modbus_id: int = 247):
        self.ip_address = ip_address
        self.modbus_id = modbus_id


class GoodWe:
    def __init__(self,
                 name: str = "GoodWe",
                 type: str = "good_we",
                 id: int = 0,
                 configuration: GoodWeConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or GoodWeConfiguration()


class GoodWeBatConfiguration:
    def __init__(self):
        pass


class GoodWeBatSetup(ComponentSetup[GoodWeBatConfiguration]):
    def __init__(self,
                 name: str = "GoodWe Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: GoodWeBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or GoodWeBatConfiguration())


class GoodWeCounterConfiguration:
    def __init__(self):
        pass


class GoodWeCounterSetup(ComponentSetup[GoodWeCounterConfiguration]):
    def __init__(self,
                 name: str = "GoodWe Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: GoodWeCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or GoodWeCounterConfiguration())


class GoodWeInverterConfiguration:
    def __init__(self):
        pass


class GoodWeInverterSetup(ComponentSetup[GoodWeInverterConfiguration]):
    def __init__(self,
                 name: str = "GoodWe Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: GoodWeInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or GoodWeInverterConfiguration())
