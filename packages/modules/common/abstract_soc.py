from abc import abstractmethod


class AbstractSoc:
    @abstractmethod
    def __init__(self, soc_config: dict) -> None:
        pass

    @abstractmethod
    def update(self, chargepoint_state) -> None:
        pass
