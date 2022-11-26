from typing import Optional

from modules.common.component_setup import ComponentSetup


class BYDConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 password: Optional[str] = None,
                 user: Optional[str] = None):
        self.password = password
        self.ip_address = ip_address
        self.user = user


class BYD:
    def __init__(self,
                 name: str = "BYD",
                 type: str = "byd",
                 id: int = 0,
                 configuration: BYDConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BYDConfiguration()


class BYDBatConfiguration:
    def __init__(self):
        pass


class BYDBatSetup(ComponentSetup[BYDBatConfiguration]):
    def __init__(self,
                 name: str = "BYD Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BYDBatConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or BYDBatConfiguration())
