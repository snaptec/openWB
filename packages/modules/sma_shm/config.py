class SpeedwireComponentConfiguration:
    def __init__(self):
        pass


class Speedwire:
    def __init__(self,
                 name: str = "SMA Home Manager",
                 type: str = "sma_shm",
                 id: int = 0,
                 configuration: SpeedwireComponentConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SpeedwireComponentConfiguration()


class SmaHomeManagerCounterConfiguration:
    def __init__(self, serials: int = None):
        self.serials = serials


class SmaHomeManagerCounterSetup:
    def __init__(self,
                 name: str = "SMA Home Manager Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmaHomeManagerCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaHomeManagerCounterConfiguration()


class SmaHomeManagerInverterConfiguration:
    def __init__(self, serials: int = None):
        self.serials = serials


class SmaHomeManagerInverterSetup:
    def __init__(self,
                 name: str = "SMA Home Manager Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmaHomeManagerInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or SmaHomeManagerInverterConfiguration()
