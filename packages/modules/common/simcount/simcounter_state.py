from typing import Iterator

from helpermodules.auto_str import auto_str


@auto_str
class SimCounterState:
    def __init__(self, timestamp: float, power: float, imported: float, exported: float):
        self.timestamp = timestamp
        self.power = power
        """In Watt"""

        self.imported = imported
        """In Watt-hours"""

        self.exported = exported
        """In Watt-hours"""

    def __iter__(self) -> Iterator[float]:
        yield self.imported
        yield self.exported
