class SolaredgeConfiguration:
    def __init__(self,
                 port: int = 502,
                 fix_only_bat_discharging: bool = False,
                 ip_address=None):
        self.port = port
        self.fix_only_bat_discharging = fix_only_bat_discharging
        self.ip_address = ip_address


class Solaredge:
    def __init__(self,
                 name: str = "SolarEdge",
                 type: str = "solaredge",
                 id: int = 0,
                 configuration:  SolaredgeConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaredgeConfiguration()


class SolaredgeBatConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class SolaredgeBatSetup:
    def __init__(self,
                 name: str = "SolarEdge Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SolaredgeBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaredgeBatConfiguration()


class SolaredgeCounterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class SolaredgeCounterSetup:
    def __init__(self,
                 name: str = "SolarEdge Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolaredgeCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaredgeCounterConfiguration()


class SolaredgeExternalInverterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class SolaredgeExternalInverterSetup:
    def __init__(self,
                 name: str = "SolarEdge externer Wechselrichter",
                 type: str = "external_inverter",
                 id: int = 0,
                 configuration: SolaredgeExternalInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaredgeExternalInverterConfiguration()


class SolaredgeInverterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class SolaredgeInverterSetup:
    def __init__(self,
                 name: str = "Solaredge Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolaredgeInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SolaredgeInverterConfiguration()
