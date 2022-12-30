from modules.common.store import get_counter_value_store
from modules.common.component_type import ComponentDescriptor
from modules.devices.discovergy.config import DiscovergyCounterSetup
from modules.devices.discovergy.utils import DiscovergyComponent


def create_component(component_config: DiscovergyCounterSetup):
    return DiscovergyComponent(component_config, get_counter_value_store(component_config.id).set)


component_descriptor = ComponentDescriptor(configuration_factory=DiscovergyCounterSetup)
