from typing import Optional


class BYDConfiguration:
    def __init__(self,
                 ip_address: Optional[str] = None,
                 password: Optional[str] = None,
                 username: Optional[str] = None):
        self.password = password
        self.ip_address = ip_address
        self.username = username


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


class BYDBatSetup:
    def __init__(self,
                 name: str = "BYD Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BYDBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BYDBatConfiguration()
