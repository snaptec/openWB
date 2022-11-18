from modules.common.component_setup import ComponentSetup


class SolaredgeConfiguration:
    def __init__(self,
                 port: int = 502,
                 ip_address=None):
        self.port = port
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


class SolaredgeBatSetup(ComponentSetup[SolaredgeBatConfiguration]):
    def __init__(self,
                 name: str = "SolarEdge Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: SolaredgeBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolaredgeBatConfiguration())


class SolaredgeCounterConfiguration:
    def __init__(self, modbus_id: int = 1, meter_id: int = 1):
        self.modbus_id = modbus_id
        self.meter_id = meter_id


class SolaredgeCounterSetup(ComponentSetup[SolaredgeCounterConfiguration]):
    def __init__(self,
                 name: str = "SolarEdge Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SolaredgeCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolaredgeCounterConfiguration())


class SolaredgeExternalInverterConfiguration:
    def __init__(self, modbus_id: int = 1, meter_id: int = 2):
        self.modbus_id = modbus_id
        self.meter_id = meter_id


class SolaredgeExternalInverterSetup(ComponentSetup[SolaredgeExternalInverterConfiguration]):
    def __init__(self,
                 name: str = "SolarEdge externer Wechselrichter",
                 type: str = "external_inverter",
                 id: int = 0,
                 configuration: SolaredgeExternalInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolaredgeExternalInverterConfiguration())


class SolaredgeInverterConfiguration:
    def __init__(self, modbus_id: int = 1):
        self.modbus_id = modbus_id


class SolaredgeInverterSetup(ComponentSetup[SolaredgeInverterConfiguration]):
    def __init__(self,
                 name: str = "SolarEdge Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SolaredgeInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SolaredgeInverterConfiguration())
