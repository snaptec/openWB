from enum import Enum


class ComponentType(Enum):
    BAT = "bat"
    CHARGEPOINT = "cp"
    COUNTER = "counter"
    INVERTER = "inverter"


def special_to_general_type_mapping(component_type: str) -> ComponentType:
    if "bat" in component_type:
        return ComponentType.BAT
    elif "counter" in component_type:
        return ComponentType.COUNTER
    elif "inverter" in component_type:
        return ComponentType.INVERTER
    elif "cp" in component_type:
        return ComponentType.CHARGEPOINT
    else:
        raise TypeError("Typ "+component_type+" konnte keinem bekannten Komponenten-Typ zugeordnet werden.")


def type_to_topic_mapping(component_type: str) -> str:
    if "bat" in component_type:
        return "bat"
    elif "counter" in component_type:
        return "counter"
    elif "inverter" in component_type:
        return "pv"
    else:
        return component_type
