from modules.common.component_setup import ComponentSetup
from modules.common import modbus


class E3dcConfiguration:
    def __init__(self, ip_address1: str = None,
                 ip_address2: str = None,
                 read_ext: int = 0,
                 pvmodul: str = None
                 ):
        self.ip_address1 = ip_address1
        self.ip_address2 = ip_address2
        self.read_ext = read_ext
        self.pvmodul = pvmodul
        # nur init hier
        self.client = modbus.ModbusTcpClient_('127.0.0.1', 502)


class E3dc:
    def __init__(self,
                 name: str = "e3dc",
                 type: str = "e3dc",
                 id: int = 0,
                 configuration: E3dcConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or E3dcConfiguration()


class E3dcBatConfiguration:
    def __init__(self):
        pass


class E3dcBatSetup(ComponentSetup[E3dcBatConfiguration]):
    def __init__(self,
                 name: str = "e3dc Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: E3dcBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration
                         or E3dcBatConfiguration())


class E3dcCounterConfiguration:
    def __init__(self):
        pass


class E3dcCounterSetup(ComponentSetup[E3dcCounterConfiguration]):
    def __init__(self,
                 name: str = "e3dc Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: E3dcCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or
                         E3dcCounterConfiguration())


class E3dcInverterConfiguration:
    def __init__(self):
        pass


class E3dcInverterSetup(ComponentSetup[E3dcInverterConfiguration]):
    def __init__(self,
                 name: str = "E3dc Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: E3dcInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or E3dcInverterConfiguration())
