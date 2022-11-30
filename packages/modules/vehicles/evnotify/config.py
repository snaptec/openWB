class EVNotifyConfiguration:
    def __init__(self, id: int = 0, akey: str = "", token: str = ""):
        self.id = id
        self.akey = akey
        self.token = token


class EVNotify:
    def __init__(self,
                 name: str = "EVNotify",
                 type: str = "evnotify",
                 configuration: EVNotifyConfiguration = None) -> None:
        self.name = name
        self.type = type
        self.configuration = configuration or EVNotifyConfiguration()
