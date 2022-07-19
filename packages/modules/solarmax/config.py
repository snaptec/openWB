from typing import Optional


class SolarmaxConfiguration:
    def __init__(self, ip_address: Optional[str] = None, modbus_id: int = 1):
        self.ip_address = ip_address
        self.modbus_id = modbus_id


class Solarmax:
    def __init__(self,
                 name: str = "Solarmax",
                 type: str = "solarmax",
                 id: int = 0,
                 configuration: SolarmaxConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolarmaxConfiguration()


class SolarmaxInverterConfiguration:
    def __init__(self):
        pass


class SolarmaxInverterSetup:
    def __init__(self,
                 name: str = "Solarmax Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolarmaxInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolarmaxInverterConfiguration()
