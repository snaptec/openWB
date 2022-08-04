from typing import Tuple, Any

from modules.common.simcount import SimCountFactory


class SimCounter:
    def __init__(self, topic: str, prefix: str):
        self.topic = topic
        self.prefix = prefix
        self.data = {}  # type: dict[str, Any]

    def sim_count(self, power: float) -> Tuple[float, float]:
        return SimCountFactory().get_sim_counter()().sim_count(power, self.topic, self.data, self.prefix)
