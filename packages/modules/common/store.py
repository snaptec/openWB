import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

try:
    from ...helpermodules import log
    from ...helpermodules import pub
except:
    # for 1.9 compability
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub


class ValueStoreFactory:
    def get_storage(self, component_type: str):
        ramdisk = Path(str(Path(os.path.abspath(__file__)).parents[3])+"/ramdisk/bootinprogress").is_file()
        if component_type == "bat":
            return BatteryValueStoreRamdisk if ramdisk else BatteryValueStoreBroker
        elif component_type == "counter":
            return CounterValueStoreRamdisk if ramdisk else CounterValueStoreBroker
        elif component_type == "inverter":
            return InverterValueStoreRamdisk if ramdisk else InverterValueStoreBroker


def write_to_file(file: str, value):
    try:
        if value != None:
            with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
                f.write(str(value))
    except Exception as e:
        log.MainLogger().error("Fehler im Modul store", e)


class ValueStore:
    @abstractmethod
    def set(self, num, values):
        pass


class BatteryValueStoreRamdisk(ValueStore):
    def set(self, num, power: float, soc: int, imported: float, exported: float):
        try:
            write_to_file("/speicherleistung", int(power))
            write_to_file("/speichersoc", int(soc))
            write_to_file("/speicherikwh", round(imported, 2))
            write_to_file("/speicherekwh", round(exported, 2))
            log.MainLogger().info('BAT Watt: ' + str(int(power)))
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)


class BatteryValueStoreBroker(ValueStore):
    def set(self, num, power: float, soc: int, imported: float, exported: float):
        try:
            pub.pub("openWB/set/bat/"+str(num)+"/get/power", round(power, 2))
            pub.pub("openWB/set/bat/"+str(num)+"/get/soc", int(soc))
            pub.pub("openWB/set/bat/"+str(num)+"/get/imported", round(imported, 2))
            pub.pub("openWB/set/bat/"+str(num)+"/get/exported", round(exported, 2))
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)


class CounterValueStoreRamdisk(ValueStore):
    def set(self, num, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            voltages = [round(val, 1) for val in voltages]
            write_to_file("/evuv1", voltages[0])
            write_to_file("/evuv2", voltages[1])
            write_to_file("/evuv3", voltages[2])
            currents = [round(val, 1) for val in currents]
            write_to_file("/bezuga1", currents[0])
            write_to_file("/bezuga2", currents[1])
            write_to_file("/bezuga3", currents[2])
            powers = [int(val) for val in powers]
            write_to_file("/bezugw1", powers[0])
            write_to_file("/bezugw2", powers[1])
            write_to_file("/bezugw3", powers[2])
            power_factors = [round(val, 2) for val in power_factors]
            write_to_file("/evupf1", power_factors[0])
            write_to_file("/evupf2", power_factors[1])
            write_to_file("/evupf3", power_factors[2])
            write_to_file("/bezugkwh", imported)
            write_to_file("/einspeisungkwh", exported)
            write_to_file("/wattbezug", int(power_all))
            write_to_file("/evuhz", round(frequency, 2))
            log.MainLogger().info('EVU Watt: ' + str(int(power_all)))
            log.MainLogger().info('EVU Bezug: ' + str(int(imported)))
            log.MainLogger().info('EVU Einspeisung: ' + str(int(exported)))
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)


class CounterValueStoreBroker(ValueStore):
    def set(self, num, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            pub.pub("openWB/set/counter/"+str(num)+"/get/voltages", [round(value, 2) for value in voltages])
            pub.pub("openWB/set/counter/"+str(num)+"/get/currents", [round(value, 2) for value in currents])
            pub.pub("openWB/set/counter/"+str(num)+"/get/power_phase", [round(value, 2) for value in powers])
            pub.pub("openWB/set/counter/"+str(num)+"/get/power_factors", [round(value, 2) for value in power_factors])
            pub.pub("openWB/set/counter/"+str(num)+"/get/imported", imported)
            pub.pub("openWB/set/counter/"+str(num)+"/get/exported", exported)
            pub.pub("openWB/set/counter/"+str(num)+"/get/power_all", power_all)
            pub.pub("openWB/set/counter/"+str(num)+"/get/frequency", frequency)
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)


class InverterValueStoreRamdisk(ValueStore):
    def set(self, num, power: float, counter: float, currents: List[float]):
        try:
            write_to_file("/pvwatt", int(power))
            write_to_file("/pvkwh", round(counter, 3))
            write_to_file("/pvkwhk", round(counter/1000, 3))
            write_to_file("/pva1", round(currents[0], 1))
            write_to_file("/pva2", round(currents[1], 1))
            write_to_file("/pva3", round(currents[2], 1))
            log.MainLogger().info('PV Watt: ' + str(int(power)))
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)


class InverterValueStoreBroker(ValueStore):
    def set(self, num, power: float, counter: float, currents: List[float]):
        try:
            pub.pub("openWB/set/pv/"+str(num)+"/get/power", round(power, 2))
            pub.pub("openWB/set/pv/"+str(num)+"/get/counter", round(counter, 3))
            currents = [round(val, 1) for val in currents]
            pub.pub("openWB/set/pv/"+str(num)+"/get/currents", currents)
        except Exception as e:
            log.MainLogger().error("Fehler im Modul store", e)
