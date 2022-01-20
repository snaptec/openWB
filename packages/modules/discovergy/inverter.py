from modules.common.component_state import InverterState, CounterState
from modules.common.store import get_inverter_value_store
from modules.discovergy.utils import DiscovergyComponent


def get_default_config(id: int = 0, **configuration) -> dict:
    return {
        "name": "Discovergy Wechselrichter",
        "id": id,
        "type": "inverter",
        "configuration": configuration
    }


def create_component(component_config: dict):
    store = get_inverter_value_store(component_config["id"])

    def persister(reading: CounterState):
        store.set(InverterState(
            counter=reading.exported,
            power=reading.power,
            currents=reading.currents
        ))

    return DiscovergyComponent(component_config, persister)
