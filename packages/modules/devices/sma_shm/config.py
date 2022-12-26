from modules.common.component_setup import ComponentSetup


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


class SmaHomeManagerCounterSetup(ComponentSetup[SmaHomeManagerCounterConfiguration]):
    def __init__(self,
                 name: str = "SMA Home Manager Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: SmaHomeManagerCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaHomeManagerCounterConfiguration())


class SmaHomeManagerInverterConfiguration:
    def __init__(self, serials: int = None):
        self.serials = serials


class SmaHomeManagerInverterSetup(ComponentSetup[SmaHomeManagerInverterConfiguration]):
    def __init__(self,
                 name: str = "SMA Home Manager Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: SmaHomeManagerInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or SmaHomeManagerInverterConfiguration())
