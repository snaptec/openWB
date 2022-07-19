class PvKitConfiguration:
    def __init__(self):
        pass


class PvKit:
    def __init__(self,
                 name: str = "PV-Kit",
                 type: str = "openwb_pv_kit",
                 id: int = 0,
                 configuration: PvKitConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PvKitConfiguration()


class PvKitInverterConfiguration:
    def __init__(self, version: int = 2):
        self.version = version


class PvKitInverterSetup:
    def __init__(self,
                 name: str = "PV-Kit",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: PvKitInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or PvKitInverterConfiguration()
