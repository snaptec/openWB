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


#class EnphaseBatConfiguration:
#    def __init__(self):
#        pass


#class EnphaseBatSetup:
#    def __init__(self,
#                 name: str = "Enphase Speicher",
#                 type: str = "bat",
#                 id: int = 0,
#                 configuration: EnphaseBatConfiguration = None) -> None:
#        self.name = name
#        self.type = type
#        self.id = id
#        self.configuration = configuration or EnphaseBatConfiguration()


class EnphaseCounterConfiguration:
    def __init__(self, eid=None):
        self.eid = eid


class EnphaseCounterSetup:
    def __init__(self,
                 name: str = "Enphase Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: EnphaseCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EnphaseCounterConfiguration()


class EnphaseInverterConfiguration:
    def __init__(self, eid=None):
        self.eid = eid


class EnphaseInverterSetup:
    def __init__(self,
                 name: str = "Enphase Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: EnphaseInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or EnphaseInverterConfiguration()
