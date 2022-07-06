from typing import Optional, Union, overload

from modules.openwb_bat_kit.config import BatKitBatSetup
from modules.openwb_evu_kit.config import EvuKitCounterSetup
from modules.openwb_pv_kit.config import PvKitInverterSetup


class FlexConfiguration:
    def __init__(self, port: int = 8899, ip_address: Optional[str] = None,):
        self.port = port
        self.ip_address = ip_address


class Flex:
    def __init__(self,
                 name: str = "OpenWB-Kit flex",
                 type: str = "openwb_flex",
                 id: int = 0,
                 configuration: FlexConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or FlexConfiguration()


class BatKitFlexConfiguration:
    def __init__(self, id: int = 117, version: int = 2):
        self.id = id
        self.version = version


class BatKitFlexSetup:
    def __init__(self,
                 name: str = "Speicher-Kit flex",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BatKitFlexConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatKitFlexConfiguration()


class EvuKitFlexConfiguration:
    def __init__(self, id: int = 115, version: int = 2):
        self.id = id
        self.version = version


class EvuKitFlexSetup:
    def __init__(self,
                 name: str = "EVU-Kit flex",
                 type: str = "counter",
                 id: int = 0,
                 configuration: EvuKitFlexConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EvuKitFlexConfiguration()


class PvKitFlexConfiguration:
    def __init__(self, id: int = 116, version: int = 2):
        self.id = id
        self.version = version


class PvKitFlexSetup:
    def __init__(self,
                 name: str = "PV-Kit flex",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: PvKitFlexConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PvKitFlexConfiguration()


@overload
def convert_to_flex_setup(kit: BatKitBatSetup, id) -> BatKitFlexSetup:
    pass


@overload
def convert_to_flex_setup(kit: EvuKitCounterSetup, id) -> EvuKitFlexSetup:
    pass


@overload
def convert_to_flex_setup(kit: PvKitInverterSetup, id) -> PvKitFlexSetup:
    pass


def convert_to_flex_setup(kit: Union[BatKitBatSetup, EvuKitCounterSetup, PvKitInverterSetup], id):
    if isinstance(kit, BatKitBatSetup):
        return BatKitFlexSetup(name=kit.name,
                               type=kit.type,
                               id=kit.id,
                               configuration=BatKitFlexConfiguration(id=id, version=kit.configuration.version))
    elif isinstance(kit, EvuKitCounterSetup):
        return EvuKitFlexSetup(name=kit.name,
                               type=kit.type,
                               id=kit.id,
                               configuration=EvuKitFlexConfiguration(id=id, version=kit.configuration.version))
    else:
        return PvKitFlexSetup(name=kit.name,
                              type=kit.type,
                              id=kit.id,
                              configuration=PvKitFlexConfiguration(id=id, version=kit.configuration.version))
