class HTTPConfiguration:
    def __init__(self, url=None):
        self.url = url


class HTTP:
    def __init__(self,
                 name: str = "HTTP",
                 type: str = "http",
                 id: int = 0,
                 configuration: HTTPConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or HTTPConfiguration()


class HttpBatConfiguration:
    def __init__(self, power_path=None, soc_path=None, imported_path=None, exported_path=None):
        self.power_path = power_path
        self.soc_path = soc_path
        self.imported_path = imported_path
        self.exported_path = exported_path


class HttpBatSetup:
    def __init__(self,
                 name: str = "HTTP Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: HttpBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or HttpBatConfiguration()


class HttpCounterConfiguration:
    def __init__(self,
                 current_l1_path=None,
                 current_l2_path=None,
                 current_l3_path=None,
                 exported_path=None,
                 imported_path=None,
                 power_path=None):
        self.current_l1_path = current_l1_path
        self.current_l2_path = current_l2_path
        self.current_l3_path = current_l3_path
        self.exported_path = exported_path
        self.imported_path = imported_path
        self.power_path = power_path


class HttpCounterSetup:
    def __init__(self,
                 name: str = "HTTP Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: HttpCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or HttpCounterConfiguration()


class HttpInverterConfiguration:
    def __init__(self, power_path=None, exported_path=None):
        self.power_path = power_path
        self.exported_path = exported_path


class HttpInverterSetup:
    def __init__(self,
                 name: str = "HTTP Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: HttpInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or HttpInverterConfiguration()
