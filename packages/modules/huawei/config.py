from typing import Optional

from modules.common.component_setup import ComponentSetup


class HuaweiConfiguration:
    def __init__(self, modbus_id: int = 1, ip_address: Optional[str] = None,):
        self.modbus_id = modbus_id
        self.ip_address = ip_address


class Huawei:
    def __init__(self,
                 name: str = "Huawei",
                 type: str = "huawei",
                 id: int = 0,
                 configuration: HuaweiConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or HuaweiConfiguration()


class HuaweiBatConfiguration:
    def __init__(self):
        pass


class HuaweiBatSetup(ComponentSetup[HuaweiBatConfiguration]):
    def __init__(self,
                 name: str = "Huawei Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: HuaweiBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HuaweiBatConfiguration())


class HuaweiCounterConfiguration:
    def __init__(self):
        pass


class HuaweiCounterSetup(ComponentSetup[HuaweiCounterConfiguration]):
    def __init__(self,
                 name: str = "Huawei Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: HuaweiCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HuaweiCounterConfiguration())


class HuaweiInverterConfiguration:
    def __init__(self):
        pass


class HuaweiInverterSetup(ComponentSetup[HuaweiInverterConfiguration]):
    def __init__(self,
                 name: str = "Huawei Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: HuaweiInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or HuaweiInverterConfiguration())
