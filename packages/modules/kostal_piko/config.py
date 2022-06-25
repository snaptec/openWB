class KostalPikoConfiguration:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address


class KostalPiko:
    def __init__(self,
                 name: str = "Kostal Piko",
                 type: str = "kostal_piko",
                 id: int = 0,
                 configuration: KostalPikoConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalPikoConfiguration()


class KostalPikoCounterConfiguration:
    def __init__(self):
        pass


class KostalPikoCounterSetup:
    def __init__(self,
                 name: str = "Kostal Piko Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: KostalPikoCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalPikoCounterConfiguration()


class KostalPikoInverterConfiguration:
    def __init__(self):
        pass


class KostalPikoInverterSetup:
    def __init__(self,
                 name: str = "Kostal Piko Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: KostalPikoInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or KostalPikoInverterConfiguration()
