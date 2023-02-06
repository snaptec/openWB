from modules.common.component_state import InverterState, CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.store import get_inverter_value_store
from modules.devices.discovergy.utils import DiscovergyComponent
from modules.devices.discovergy.config import DiscovergyInverterSetup


def create_component(component_config: DiscovergyInverterSetup):
    store = get_inverter_value_store(component_config.id)

    def persister(reading: CounterState):
        store.set(InverterState(
            exported=reading.exported,
            power=reading.power,
            currents=reading.currents
        ))

    return DiscovergyComponent(component_config, persister)


component_descriptor = ComponentDescriptor(configuration_factory=DiscovergyInverterSetup)
