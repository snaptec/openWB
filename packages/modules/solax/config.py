from typing import Optional


class SolaxConfiguration:
    def __init__(self, modbus_id: int = 1, ip_address: Optional[str] = None,):
        self.modbus_id = modbus_id
        self.ip_address = ip_address


class Solax:
    def __init__(self,
                 name: str = "Solax",
                 type: str = "solax",
                 id: int = 0,
                 configuration: SolaxConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaxConfiguration()


class SolaxBatConfiguration:
    def __init__(self):
        pass


class SolaxBatSetup:
    def __init__(self,
                 name: str = "Solax Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SolaxBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaxBatConfiguration()


class SolaxCounterConfiguration:
    def __init__(self):
        pass


class SolaxCounterSetup:
    def __init__(self,
                 name: str = "Solax Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolaxCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaxCounterConfiguration()


class SolaxInverterConfiguration:
    def __init__(self):
        pass


class SolaxInverterSetup:
    def __init__(self,
                 name: str = "Solax Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolaxInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaxInverterConfiguration()
