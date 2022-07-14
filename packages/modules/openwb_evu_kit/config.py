from modules.openwb_bat_kit.config import BatKitBatSetup
from modules.openwb_pv_kit.config import PvKitInverterSetup


class EvuKitConfiguration:
    def __init__(self):
        pass


class EvuKit:
    def __init__(self,
                 name: str = "EVU-Kit",
                 type: str = "openwb_evu_kit",
                 id: int = 0,
                 configuration: EvuKitConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EvuKitConfiguration()


class EvuKitBatConfiguration:
    def __init__(self, version: int = 2):
        self.version = version


class EvuKitBatSetup(BatKitBatSetup):
    def __init__(self,
                 name: str = "Speicher-Zähler an EVU-Kit",
                 type: str = "bat",
                 id: int = 0,
                 configuration: EvuKitBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EvuKitBatConfiguration()


class EvuKitCounterConfiguration:
    def __init__(self, version: int = 2):
        self.version = version


class EvuKitCounterSetup:
    def __init__(self,
                 name: str = "EVU-Kit",
                 type: str = "counter",
                 id: int = 0,
                 configuration: EvuKitCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EvuKitCounterConfiguration()


class EvuKitInverterConfiguration:
    def __init__(self, version: int = 2):
        self.version = version


class EvuKitInverterSetup(PvKitInverterSetup):
    def __init__(self,
                 name: str = "PV-Zähler an EVU-Kit",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: EvuKitInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EvuKitInverterConfiguration()
