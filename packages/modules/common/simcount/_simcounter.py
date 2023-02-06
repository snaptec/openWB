from typing import Tuple, Optional

from modules.common.simcount._simcount import sim_count
from modules.common.simcount.simcounter_state import SimCounterState


class SimCounter:
    def __init__(self, device_id: int, component_id: int, prefix: str):
        self.topic = "openWB/set/system/device/{}/component/{}/".format(device_id, component_id)
        self.prefix = "pv2" if prefix == "pv" and component_id != 1 else prefix
        self.data = None  # type: Optional[SimCounterState]

    def sim_count(self, power: float) -> Tuple[float, float]:
        self.data = sim_count(power, self.topic, self.data, self.prefix)
        return self.data.imported, self.data.exported
