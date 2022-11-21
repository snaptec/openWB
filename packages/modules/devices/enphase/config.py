from modules.common.component_setup import ComponentSetup


class EnphaseConfiguration:
    def __init__(self, hostname=None):
        self.hostname = hostname


class Enphase:
    def __init__(self,
                 name: str = "Enphase",
                 type: str = "enphase",
                 id: int = 0,
                 configuration: EnphaseConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EnphaseConfiguration()


class EnphaseCounterConfiguration:
    def __init__(self, eid=None):
        self.eid = eid


class EnphaseCounterSetup(ComponentSetup[EnphaseCounterConfiguration]):
    def __init__(self,
                 name: str = "Enphase Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: EnphaseCounterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or EnphaseCounterConfiguration())


class EnphaseInverterConfiguration:
    def __init__(self, eid=None):
        self.eid = eid


class EnphaseInverterSetup(ComponentSetup[EnphaseInverterConfiguration]):
    def __init__(self,
                 name: str = "Enphase Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: EnphaseInverterConfiguration = None) -> None:
        super().__init__(name, type, id, configuration or EnphaseInverterConfiguration())
