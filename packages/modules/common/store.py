from abc import abstractmethod
from collections.abc import Iterable
from typing import Callable, Generic, TypeVar, Union

from helpermodules import compatibility
from helpermodules import log
from helpermodules import pub
from modules.common.component_state import BatState, CounterState, InverterState
from modules.common.fault_state import FaultState


def process_error(e):
    raise FaultState.error(__name__+" "+str(type(e))+" "+str(e)) from e


def write_array_to_files(prefix: str, values: Iterable, digits: int = None):
    for index, value in enumerate(values):
        write_to_file(prefix+str(index + 1), value, digits)


def write_to_file(file: str, value, digits: Union[int, None] = None) -> None:
    try:
        rounding = get_rounding_function_by_digits(digits)
        with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
            f.write(str(rounding(value)))
        return value
    except Exception as e:
        process_error(e)


def get_rounding_function_by_digits(digits: Union[int, None]) -> Callable:
    if digits is None:
        return lambda value: value
    elif digits == 0:
        return int
    else:
        return lambda value: round(value, digits)


def pub_to_broker(topic: str, value, digits: Union[int, None] = None) -> None:
    rounding = get_rounding_function_by_digits(digits)
    try:
        if isinstance(value, list):
            pub.pub(topic, [rounding(v) for v in value])
        else:
            pub.pub(topic, rounding(value))
    except Exception as e:
        process_error(e)


T = TypeVar("T")


class ValueStore(Generic[T]):
    @abstractmethod
    def set(self, state: T) -> None:
        pass


class BatteryValueStoreRamdisk(ValueStore[BatState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, bat_state: BatState):
        try:
            power = write_to_file("/speicherleistung", bat_state.power, 0)
            write_to_file("/speichersoc", bat_state.soc, 0)
            write_to_file("/speicherikwh", bat_state.imported, 2)
            write_to_file("/speicherekwh", bat_state.exported, 2)
            log.MainLogger().info('BAT Watt: ' + str(power))
            log.MainLogger().info('BAT Einspeisung: ' + str(bat_state.exported))
            log.MainLogger().info('BAT Bezug: ' + str(bat_state.imported))
        except Exception as e:
            process_error(e)


class BatteryValueStoreBroker(ValueStore[BatState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, bat_state: BatState):
        try:
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/power", bat_state.power, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/soc", bat_state.soc, 0)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/imported", bat_state.imported, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/exported", bat_state.exported, 2)
        except Exception as e:
            process_error(e)


class CounterValueStoreRamdisk(ValueStore[CounterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, counter_state: CounterState):
        try:
            write_array_to_files("/evuv", counter_state.voltages, 1)
            write_array_to_files("/bezuga", counter_state.currents, 1)
            write_array_to_files("/bezugw", counter_state.powers, 0)
            write_array_to_files("/evupf", counter_state.power_factors, 2)
            imported = write_to_file("/bezugkwh", counter_state.imported)
            exported = write_to_file("/einspeisungkwh", counter_state.exported)
            power_all = write_to_file("/wattbezug", counter_state.power_all, 0)
            write_to_file("/evuhz", counter_state.frequency, 2)
            log.MainLogger().info('EVU Watt: ' + str(power_all))
            log.MainLogger().info('EVU Bezug: ' + str(imported))
            log.MainLogger().info('EVU Einspeisung: ' + str(exported))
        except Exception as e:
            process_error(e)


class CounterValueStoreBroker(ValueStore[CounterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, counter_state: CounterState):
        try:
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/voltage", counter_state.voltages, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/current", counter_state.currents, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_phase", counter_state.powers, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_factors", counter_state.power_factors, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/imported", counter_state.imported)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/exported", counter_state.exported)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_all", counter_state.power_all)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/frequency", counter_state.frequency)
        except Exception as e:
            process_error(e)


class InverterValueStoreRamdisk(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, inverter_state: InverterState):
        try:
            if self.num == 1:
                filename_extension = ""
            elif self.num == 2:
                filename_extension = "2"
            else:
                raise FaultState.error("Unbekannte PV-Nummer "+str(self.num))
            power = write_to_file("/pv"+filename_extension+"watt", inverter_state.power, 0)
            write_to_file("/pv"+filename_extension+"kwh", inverter_state.counter, 3)
            write_to_file("/pv"+filename_extension+"kwhk", inverter_state.counter/1000, 3)
            write_array_to_files("/pv"+filename_extension+"a", inverter_state.currents, 1)
            log.MainLogger().info('PV Watt: ' + str(power))
        except Exception as e:
            process_error(e)


class InverterValueStoreBroker(ValueStore[InverterState]):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, inverter_state: InverterState):
        try:
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/power", inverter_state.power, 2)
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/counter", inverter_state.counter, 3)
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/currents", inverter_state.currents, 1)
        except Exception as e:
            process_error(e)


def get_bat_value_store(component_num: int) -> ValueStore[BatState]:
    if compatibility.is_ramdisk_in_use():
        return BatteryValueStoreRamdisk(component_num)
    else:
        return BatteryValueStoreBroker(component_num)


def get_counter_value_store(component_num: int) -> ValueStore[CounterState]:
    if compatibility.is_ramdisk_in_use():
        return CounterValueStoreRamdisk(component_num)
    else:
        return CounterValueStoreBroker(component_num)


def get_inverter_value_store(component_num: int) -> ValueStore[InverterState]:
    if compatibility.is_ramdisk_in_use():
        return InverterValueStoreRamdisk(component_num)
    else:
        return InverterValueStoreBroker(component_num)
