from modules.common.component_setup import ComponentSetup


class e3dcConfiguration:
    def __init__(self, ip_address1: str = None,
                 ip_address2: str = None,
                 read_ext: int = 0,
                 pvmodul: str = None):
        self.ip_address1 = ip_address1
        self.ip_address2 = ip_address2
        self.read_ext = read_ext
        self.pvmodul = pvmodul


class e3dc:
    def __init__(self,
                 name: str = "e3dc",
                 type: str = "e3dc",
                 id: int = 0,
                 configuration: e3dcConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or e3dcConfiguration()


class e3dcBatConfiguration:
    def __init__(self):
        pass


class e3dcBatSetup(ComponentSetup[e3dcBatConfiguration]):
    def __init__(self,
                 name: str = "e3dc Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: e3dcBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration
                         or e3dcBatConfiguration())


class e3dcCounterConfiguration:
    def __init__(self):
        pass


class e3dcCounterSetup(ComponentSetup[e3dcCounterConfiguration]):
    def __init__(self,
                 name: str = "e3dc Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: e3dcCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or
                         e3dcCounterConfiguration())
