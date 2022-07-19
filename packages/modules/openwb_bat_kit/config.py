class BatKitConfiguration:
    def __init__(self):
        pass


class BatKit:
    def __init__(self,
                 name: str = "Speicher-Kit",
                 type: str = "openwb_bat_kit",
                 id: int = 0,
                 configuration: BatKitConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatKitConfiguration()


class BatKitBatConfiguration:
    def __init__(self, version: int = 2):
        self.version = version


class BatKitBatSetup:
    def __init__(self,
                 name: str = "Speicher-Kit",
                 type: str = "bat",
                 id: int = 0,
                 configuration: BatKitBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or BatKitBatConfiguration()
