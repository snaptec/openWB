from abc import abstractmethod


class AbstractChargepoint:
    @abstractmethod
    def __init__(self, id: int, connection_module: dict, power_module: dict) -> None:
        pass

    @abstractmethod
    def set_current(self, current: float) -> None:
        pass

    @abstractmethod
    def get_values(self) -> None:
        pass

    @abstractmethod
    def switch_phases(self, phases_to_use: int, duration: int) -> None:
        pass

    @abstractmethod
    def interrupt_cp(self, duration: int) -> None:
        pass

    @abstractmethod
    def clear_rfid(self) -> None:
        pass
