from typing import Optional

from modules.common.component_setup import ComponentSetup


class TeslaConfiguration:
    def __init__(self, password: Optional[str] = None, email: Optional[str] = None, ip_address: Optional[str] = None):
        self.password = password
        self.email = email
        self.ip_address = ip_address


class Tesla:
    def __init__(self,
                 name: str = "Tesla",
                 type: str = "tesla",
                 id: int = 0,
                 configuration: TeslaConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or TeslaConfiguration()


class TeslaBatConfiguration:
    def __init__(self):
        pass


class TeslaBatSetup(ComponentSetup[TeslaBatConfiguration]):
    def __init__(self,
                 name: str = "Tesla Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: TeslaBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or TeslaBatConfiguration())


class TeslaCounterConfiguration:
    def __init__(self):
        pass


class TeslaCounterSetup(ComponentSetup[TeslaCounterConfiguration]):
    def __init__(self,
                 name: str = "Tesla Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: TeslaCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or TeslaCounterConfiguration())


class TeslaInverterConfiguration:
    def __init__(self):
        pass


class TeslaInverterSetup(ComponentSetup[TeslaInverterConfiguration]):
    def __init__(self,
                 name: str = "Tesla Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: TeslaInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or TeslaInverterConfiguration())
