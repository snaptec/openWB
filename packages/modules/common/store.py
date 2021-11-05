from abc import abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import List

try:
    from ..common.module_error import ModuleError, ModuleErrorLevels
    from ...helpermodules import compability
    from ...helpermodules import log
    from ...helpermodules import pub
except:
    # for 1.9 compability
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import compability
    from helpermodules import log
    from helpermodules import pub
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class ValueStoreFactory:
    def get_storage(self, component_type: str):
        try:
            ramdisk = compability.check_ramdisk_usage()
            if component_type == "bat":
                return BatteryValueStoreRamdisk if ramdisk else BatteryValueStoreBroker
            elif component_type == "counter":
                return CounterValueStoreRamdisk if ramdisk else CounterValueStoreBroker
            elif component_type == "inverter":
                return InverterValueStoreRamdisk if ramdisk else InverterValueStoreBroker
        except Exception as e:
            process_error(e)


def process_error(e):
    raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevels.ERROR) from e


def write_array_to_files(prefix: str, values: Iterable, digits: int = None):
    for index, value in enumerate(values):
        write_to_file(prefix+str(index + 1), value, digits)


def write_to_file(file: str, value, digits: int = None) -> None:
    try:
        if digits != None:
            if digits == 0:
                value = int(value)
            else:
                value = round(value, digits)
        with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
            f.write(str(value))
        return value
    except Exception as e:
        process_error(e)


def pub_to_broker(topic: str, value, digits: int = None) -> None:
    try:
        if isinstance(value, list):
            if digits != None:
                if digits == 0:
                    value = [int(val,) for val in value]
                else:
                    value = [round(val, digits) for val in value]
            pub.pub(topic, value)
        else:
            if digits != None:
                if digits == 0:
                    value = int(value)
                else:
                    value = round(value, digits)
            pub.pub(topic, value)
    except Exception as e:
        process_error(e)


class ValueStore:
    @abstractmethod
    def set(self, *kwargs) -> None:
        pass


class BatteryValueStoreRamdisk(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, power: float, soc: int, imported: float, exported: float):
        try:
            power = write_to_file("/speicherleistung", power, 0)
            write_to_file("/speichersoc", soc, 0)
            write_to_file("/speicherikwh", imported, 2)
            write_to_file("/speicherekwh", exported, 2)
            log.MainLogger().info('BAT Watt: ' + str(power))
            log.MainLogger().info('BAT Einspeisung: ' + str(exported))
            log.MainLogger().info('BAT Bezug: ' + str(imported))
        except Exception as e:
            process_error(e)


class BatteryValueStoreBroker(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, power: float, soc: int, imported: float, exported: float):
        try:
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/power", power, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/soc", soc, 0)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/imported", imported, 2)
            pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/exported", exported, 2)
        except Exception as e:
            process_error(e)


class CounterValueStoreRamdisk(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            write_array_to_files("/evuv", voltages, 1)
            write_array_to_files("/bezuga", currents, 1)
            write_array_to_files("/bezugw", powers, 0)
            write_array_to_files("/evupf", power_factors, 2)
            imported = write_to_file("/bezugkwh", imported)
            exported = write_to_file("/einspeisungkwh", exported)
            power_all = write_to_file("/wattbezug", power_all, 0)
            write_to_file("/evuhz", frequency, 2)
            log.MainLogger().info('EVU Watt: ' + str(power_all))
            log.MainLogger().info('EVU Bezug: ' + str(imported))
            log.MainLogger().info('EVU Einspeisung: ' + str(exported))
        except Exception as e:
            process_error(e)


class CounterValueStoreBroker(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/voltage", voltages, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/current", currents, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_phase", powers, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_factors", power_factors, 2)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/imported", imported)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/exported", exported)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_all", power_all)
            pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/frequency", frequency)
        except Exception as e:
            process_error(e)


class InverterValueStoreRamdisk(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, power: float, counter: float, currents: List[float]):
        try:
            if self.num == 1:
                filename_extension = ""
            elif self.num == 2:
                filename_extension = "2"
            else:
                log.MainLogger().error("Unbekannte PV-Nummer "+str(self.num))
            power = write_to_file("/pv"+filename_extension+"watt", power, 0)
            write_to_file("/pv"+filename_extension+"kwh", counter, 3)
            write_to_file("/pv"+filename_extension+"kwhk", counter/1000, 3)
            write_array_to_files("/pv"+filename_extension+"a", currents, 1)
            log.MainLogger().info('PV Watt: ' + str(power))
        except Exception as e:
            process_error(e)


class InverterValueStoreBroker(ValueStore):
    def __init__(self, component_num: int) -> None:
        self.num = component_num

    def set(self, power: float, counter: float, currents: List[float]):
        try:
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/power", power, 2)
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/counter", counter, 3)
            pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/currents", currents, 1)
        except Exception as e:
            process_error(e)
