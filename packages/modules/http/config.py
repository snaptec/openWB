from helpermodules.auto_str import auto_str
from modules.common.component_setup import ComponentSetup


@auto_str
class HTTPConfiguration:
    def __init__(self, url=None):
        self.url = url


@auto_str
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


@auto_str
class HttpBatConfiguration:
    def __init__(self, power_path=None, soc_path=None, imported_path=None, exported_path=None):
        self.power_path = power_path
        self.soc_path = soc_path
        self.imported_path = imported_path
        self.exported_path = exported_path


@auto_str
class HttpBatSetup(ComponentSetup[HttpBatConfiguration]):
    def __init__(self,
                 name: str = "HTTP Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: HttpBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HttpBatConfiguration())


@auto_str
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


@auto_str
class HttpCounterSetup(ComponentSetup[HttpCounterConfiguration]):
    def __init__(self,
                 name: str = "HTTP Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: HttpCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HttpCounterConfiguration())


@auto_str
class HttpInverterConfiguration:
    def __init__(self, power_path=None, exported_path=None):
        self.power_path = power_path
        self.exported_path = exported_path


@auto_str
class HttpInverterSetup(ComponentSetup[HttpInverterConfiguration]):
    def __init__(self,
                 name: str = "HTTP Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: HttpInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HttpInverterConfiguration())
