from modules.common.store import get_counter_value_store
from modules.discovergy.utils import DiscovergyComponent


def get_default_config(**configuration) -> dict:
    return {
        "name": "Discovergy Zähler",
        "id": 0,
        "type": "counter",
        "configuration": configuration
    }


def create_component(component_config: dict):
    return DiscovergyComponent(component_config, get_counter_value_store(component_config["id"]).set)
