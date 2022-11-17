from typing import Callable, Union
from requests import Session

from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.devices.discovergy.api import get_last_reading
from modules.devices.discovergy.config import DiscovergyCounterSetup, DiscovergyInverterSetup


class DiscovergyComponent:
    def __init__(self,
                 component_config: Union[DiscovergyCounterSetup, DiscovergyInverterSetup],
                 persister: Callable[[CounterState], None]):
        self.__meter_id = component_config.configuration.meter_id
        self.store = persister
        self.component_info = ComponentInfo.from_component_config(component_config)
        self.component_config = component_config

    def update(self, session: Session):
        self.store(get_last_reading(session, self.__meter_id))
