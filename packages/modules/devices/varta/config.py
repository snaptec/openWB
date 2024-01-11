from typing import Optional
from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup


@auto_str
class VartaConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


@auto_str
class Varta:
    def __init__(self,
                 name: str = "Varta",
                 type: str = "varta",
                 id: int = 0,
                 configuration: VartaConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or VartaConfiguration()


@auto_str
class VartaBatApiConfiguration:
    def __init__(self):
        pass


@auto_str
class VartaBatApiSetup(ComponentSetup[VartaBatApiConfiguration]):
    def __init__(self,
                 name: str = "Varta Speicher (Abfrage per API)",
                 type: str = "bat_api",
                 id: int = 0,
                 configuration: VartaBatApiConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VartaBatApiConfiguration())


@auto_str
class VartaBatModbusConfiguration:
    def __init__(self):
        pass


@auto_str
class VartaBatModbusSetup(ComponentSetup[VartaBatModbusConfiguration]):
    def __init__(self,
                 name: str = "Speicher Varta Pulse, Element, Neo, u.a. (Abfrage per Modbus)",
                 type: str = "bat_modbus",
                 id: int = 0,
                 configuration: VartaBatModbusConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VartaBatModbusConfiguration())


@auto_str
class VartaCounterConfiguration:
    def __init__(self):
        pass


@auto_str
class VartaCounterSetup(ComponentSetup[VartaCounterConfiguration]):
    def __init__(self,
                 name: str = "Varta Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: VartaCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or VartaCounterConfiguration())
