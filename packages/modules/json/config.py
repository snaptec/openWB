class JsonConfiguration:
    def __init__(self, url=None):
        self.url = url


class Json:
    def __init__(self,
                 name: str = "Json",
                 type: str = "json",
                 id: int = 0,
                 configuration: JsonConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or JsonConfiguration()


class JsonBatConfiguration:
    def __init__(self, jq_imported=None, jq_exported=None, jq_soc=None, jq_power=None,):
        self.jq_imported = jq_imported
        self.jq_exported = jq_exported
        self.jq_soc = jq_soc
        self.jq_power = jq_power


class JsonBatSetup:
    def __init__(self,
                 name: str = "Json Speicher",
                 type: str = "bat",
                 id: int = 0,
                 configuration: JsonBatConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or JsonBatConfiguration()


class JsonCounterConfiguration:
    def __init__(self, jq_power=None, jq_exported=None, jq_imported=None,):
        self.jq_power = jq_power
        self.jq_exported = jq_exported
        self.jq_imported = jq_imported


class JsonCounterSetup:
    def __init__(self,
                 name: str = "Json Zähler",
                 type: str = "counter",
                 id: int = 0,
                 configuration: JsonCounterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or JsonCounterConfiguration()


class JsonInverterConfiguration:
    def __init__(self, jq_power=None, jq_exported=None):
        self.jq_power = jq_power
        self.jq_exported = jq_exported


class JsonInverterSetup:
    def __init__(self,
                 name: str = "Json Wechselrichter",
                 type: str = "inverter",
                 id: int = 0,
                 configuration: JsonInverterConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration or JsonInverterConfiguration()
