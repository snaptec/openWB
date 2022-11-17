from typing import Optional

from modules.common.component_setup import ComponentSetup


class StuderConfiguration:
    def __init__(self, ip_address: Optional[str] = None):
        self.ip_address = ip_address


class Studer:
    def __init__(self,
                 name: str = "Studer",
                 type: str = "studer",
                 id: int = 0,
                 configuration: StuderConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or StuderConfiguration()


class StuderBatConfiguration:
    def __init__(self):
        pass


class StuderBatSetup(ComponentSetup[StuderBatConfiguration]):
    def __init__(self,
                 name: str = "Studer Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: StuderBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or StuderBatConfiguration())


class StuderInverterConfiguration:
    def __init__(self, vc_count=1, vc_type="VS"):
        self.vc_count = vc_count  # studer_vc (count MPPT Devices)
        self.vc_type = vc_type  # studer_vc_type (MPPT type VS or VT))


class StuderInverterSetup(ComponentSetup[StuderInverterConfiguration]):
    def __init__(self,
                 name: str = "Studer Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: StuderInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or StuderInverterConfiguration())
