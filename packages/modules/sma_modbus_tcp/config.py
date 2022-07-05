from modules.sma_modbus_tcp.inverter_version import SmaInverterVersion


class SmaModbusTcpConfiguration:
    def __init__(self, ip_address=None):
        self.ip_address = ip_address


class SmaModbusTcp:
    def __init__(self,
                 name: str = "SMA ModbusTCP",
                 type: str = "sma_modbus_tcp",
                 id: int = 0,
                 configuration: SmaModbusTcpConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaModbusTcpConfiguration()


class SmaModbusTcpInverterConfiguration:
    def __init__(self, version=SmaInverterVersion.default.value, hybrid=False):
        self.version = version
        self.hybrid = hybrid


class SmaModbusTcpInverterSetup:
    def __init__(self,
                 name: str = "SMA ModbusTCP Wechselrichter",
                 type: str = "inverter_modbus_tcp",
                 id: int = 0,
                 configuration: SmaModbusTcpInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaModbusTcpInverterConfiguration()


class SmaWebboxInverterConfiguration:
    def __init__(self):
        pass


class SmaWebboxInverterSetup:
    def __init__(self,
                 name: str = "SMA Wechselrichter Webbox",
                 type: str = "inverter_webbox",
                 id: int = 0,
                 configuration: SmaWebboxInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaWebboxInverterConfiguration()
