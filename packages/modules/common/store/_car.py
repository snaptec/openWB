from modules.common.component_state import CarState
from modules.common.store import ValueStore
from modules.common.store._api import LoggingValueStore
from modules.common.store.ramdisk import files


class CarValueStoreRamdisk(ValueStore[CarState]):
    def __init__(self, charge_point: int):
        self.file = files.charge_points[charge_point - 1].soc

    def set(self, state: CarState) -> None:
        self.file.write(int(state.soc))


def get_car_value_store(id: int) -> ValueStore[CarState]:
    return LoggingValueStore(CarValueStoreRamdisk(id))
