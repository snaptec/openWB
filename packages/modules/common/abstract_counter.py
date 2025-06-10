from abc import abstractmethod
from typing import List, Tuple

from modules.common import modbus


class AbstractCounter:
    @abstractmethod
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        pass

    @abstractmethod
    def get_currents(self) -> List[float]:
        return [0]*3

    @abstractmethod
    def get_exported(self) -> float:
        return 0

    @abstractmethod
    def get_frequency(self) -> float:
        return 50

    @abstractmethod
    def get_imported(self) -> float:
        return 0

    @abstractmethod
    def get_power(self) -> Tuple[List[float], float]:
        return [0]*3, 0

    @abstractmethod
    def get_power_factors(self) -> List[float]:
        return [0]*3

    @abstractmethod
    def get_voltages(self) -> List[float]:
        return [230]*3
