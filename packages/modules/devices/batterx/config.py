from typing import Optional

from modules.common.component_setup import ComponentSetup


class BatterXConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class BatterX:
    def __init__(self,
                 name: str = "BatterX",
                 type: str = "batterx",
                 id: int = 0,
                 configuration: BatterXConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatterXConfiguration()


class BatterXBatConfiguration:
    def __init__(self):
        pass


class BatterXBatSetup(ComponentSetup[BatterXBatConfiguration]):
    def __init__(self,
                 name: str = "BatterX Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BatterXBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or BatterXBatConfiguration())


class BatterXCounterConfiguration:
    def __init__(self):
        pass


class BatterXCounterSetup(ComponentSetup[BatterXCounterConfiguration]):
    def __init__(self,
                 name: str = "BatterX Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: BatterXCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or BatterXCounterConfiguration())


class BatterXExternalInverterConfiguration:
    def __init__(self):
        pass


class BatterXExternalInverterSetup(ComponentSetup[BatterXExternalInverterConfiguration]):
    def __init__(self,
                 name: str = "BatterX externer Wechselrichter",
                 type: str = "external_inverter",
                 id: int = 0,
                 configuration: BatterXExternalInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or BatterXExternalInverterConfiguration())


class BatterXInverterConfiguration:
    def __init__(self):
        pass


class BatterXInverterSetup(ComponentSetup[BatterXInverterConfiguration]):
    def __init__(self,
                 name: str = "BatterX Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: BatterXInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or BatterXInverterConfiguration())
