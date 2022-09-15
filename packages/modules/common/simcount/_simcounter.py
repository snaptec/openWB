from typing import Tuple, Any

from modules.common.simcount import SimCountFactory


class SimCounter:
    def __init__(self, device_id: int, component_id: int, prefix: str):
        self.topic = "openWB/set/system/device/{}/component/{}/".format(device_id, component_id)
        self.prefix = "pv2" if prefix == "pv" and component_id != 1 else prefix
        self.data = {}  # type: dict[str, Any]

    def sim_count(self, power: float) -> Tuple[float, float]:
        return SimCountFactory().get_sim_counter()().sim_count(power, self.topic, self.data, self.prefix)
