import os
import paho.mqtt.publish as publish
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


class ValueStore:
    @abstractmethod
    def set(self, values):
        pass

    def write_to_file(self, file: str, value, digits: int = None) -> float:
        try:
            if isinstance(value, (int, float)):
                if digits != None:
                    if digits == 0:
                        value = int(value)
                    else:
                        value = round(value, digits)
                with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
                    f.write(str(value))
            else:
                self.set_error(value)
            return value
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")

    def pub_to_broker(self, topic: str, value, digits: int = None) -> None:
        try:
            if isinstance(value, list):
                if all(isinstance(x, (int, float)) for x in value):
                    if digits != None:
                        if digits == 0:
                            value = [int(val,) for val in value]
                        else:
                            value = [round(val, digits) for val in value]
                else:
                    self.set_error(value)

            else:
                if isinstance(value, (int, float)):
                    if digits != None:
                        if digits == 0:
                            value = int(value)
                        else:
                            value = round(value, digits)
                else:
                    self.set_error(value)
            pub.pub(topic, value)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")

    def reset_error(self) -> None:
        try:
            if self.is_error_set == False:
                ramdisk = Path(str(Path(os.path.abspath(__file__)).parents[3])+"/ramdisk/bootinprogress").is_file()
                if ramdisk == True:
                    if self.num != None:
                        publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/faultState", 0)
                        publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/faultStr", "Kein Fehler.")
                    else:
                        publish.single("openWB/set/"+self.type+"/faultState", 0)
                        publish.single("openWB/set/"+self.type+"/faultStr", "Kein Fehler.")
                else:
                    pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_str", "Kein Fehler.")
                    pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_state", 0)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")

    def set_error(self, value: dict) -> None:
        try:
            # Nur beim ersten Fehler je Zyklus publishen
            if self.is_error_set == False:
                log.MainLogger().debug("Fehlerstring publishen: "+str(value))
                ramdisk = Path(str(Path(os.path.abspath(__file__)).parents[3])+"/ramdisk/bootinprogress").is_file()
                if ramdisk == True:
                    if self.num != None:
                        try:
                            publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/get/faultStr", value["fault_str"])
                            publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/get/faultState", value["fault_state"])
                        except:
                            publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/get/faultStr", "Es ist ein interner Fehler aufgetreten.")
                            publish.single("openWB/set/"+self.type+"/"+str(self.num)+"/get/faultState", 2)
                    else:
                        try:
                            publish.single("openWB/set/"+self.type+"/get/faultStr", value["fault_str"])
                            publish.single("openWB/set/"+self.type+"/get/faultState", value["fault_state"])
                        except:
                            publish.single("openWB/set/"+self.type+"/get/faultStr", "Es ist ein interner Fehler aufgetreten.")
                            publish.single("openWB/set/"+self.type+"/get/faultState", 2)
                else:
                    try:
                        pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_str", value["fault_str"])
                        pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_state", value["fault_state"])
                    except:
                        pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_str", "Es ist ein interner Fehler aufgetreten.")
                        pub.pub("openWB/set/"+self.type+"/"+str(self.num)+"/get/fault_state", 2)
                self.is_error_set = True
        except:
            log.MainLogger().exception(self.name)


class BatteryValueStoreRamdisk(ValueStore):
    def __init__(self, num) -> None:
        self.num = None
        self.type = "houseBattery"
        super().__init__()

    def set(self, power: float, soc: int, imported: float, exported: float):
        try:
            self.error_set = False
            power = self.write_to_file("/speicherleistung", power, 0)
            self.write_to_file("/speichersoc", soc, 0)
            self.write_to_file("/speicherikwh", imported, 2)
            self.write_to_file("/speicherekwh", exported, 2)
            log.MainLogger().info('BAT Watt: ' + str(power))
            log.MainLogger().info('BAT Einspeisung: ' + str(exported))
            log.MainLogger().info('BAT Bezug: ' + str(imported))
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")


class BatteryValueStoreBroker(ValueStore):
    def __init__(self, num) -> None:
        self.num = num
        self.type = "bat"
        super().__init__()

    def set(self, power: float, soc: int, imported: float, exported: float):
        try:
            self.is_error_set = False
            self.pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/power", power, 2)
            self.pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/soc", soc, 0)
            self.pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/imported", imported, 2)
            self.pub_to_broker("openWB/set/bat/"+str(self.num)+"/get/exported", exported, 2)
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")


class CounterValueStoreRamdisk(ValueStore):
    def __init__(self, num) -> None:
        self.num = None
        self.type = "evu"
        super().__init__()

    def set(self, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            self.is_error_set = False
            self.write_to_file("/evuv1", voltages[0], 1)
            self.write_to_file("/evuv2", voltages[1], 1)
            self.write_to_file("/evuv3", voltages[2], 1)
            self.write_to_file("/bezuga1", currents[0], 1)
            self.write_to_file("/bezuga2", currents[1], 1)
            self.write_to_file("/bezuga3", currents[2], 1)
            self.write_to_file("/bezugw1", powers[0], 0)
            self.write_to_file("/bezugw2", powers[1], 0)
            self.write_to_file("/bezugw3", powers[2], 0)
            self.write_to_file("/evupf1", power_factors[0], 2)
            self.write_to_file("/evupf2", power_factors[1], 2)
            self.write_to_file("/evupf3", power_factors[2], 2)
            imported = self.write_to_file("/bezugkwh", imported)
            exported = self.write_to_file("/einspeisungkwh", exported)
            power_all = self.write_to_file("/wattbezug", power_all, 0)
            self.write_to_file("/evuhz", frequency, 2)
            log.MainLogger().info('EVU Watt: ' + str(power_all))
            log.MainLogger().info('EVU Bezug: ' + str(imported))
            log.MainLogger().info('EVU Einspeisung: ' + str(exported))
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")


class CounterValueStoreBroker(ValueStore):
    def __init__(self, num) -> None:
        self.num = num
        self.type = "counter"
        super().__init__()

    def set(self, voltages: List[float], currents: List[float], powers: List[float], power_factors: List[float], imported: float, exported: float, power_all: float, frequency: float):
        try:
            self.is_error_set = False
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/voltage", voltages, 2)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/current", currents, 2)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_phase", powers, 2)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_factors", power_factors, 2)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/imported", imported)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/exported", exported)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/power_all", power_all)
            self.pub_to_broker("openWB/set/counter/"+str(self.num)+"/get/frequency", frequency)
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")


class InverterValueStoreRamdisk(ValueStore):
    def __init__(self, num) -> None:
        self.num = num
        self.type = "pv"
        super().__init__()

    def set(self, power: float, counter: float, currents: List[float]):
        try:
            if self.num == 1:
                filename_extension = ""
            elif self.num == 2:
                filename_extension = "2"
            else:
                log.MainLogger().error("Unbekannte PV-Nummer "+str(self.num))
            self.is_error_set = False
            power = self.write_to_file("/pv"+filename_extension+"watt", power, 0)
            self.write_to_file("/pv"+filename_extension+"kwh", counter, 3)
            if isinstance(counter, (int, float)):
                self.write_to_file("/pv"+filename_extension+"kwhk", counter/1000, 3)
            self.write_to_file("/pv"+filename_extension+"a1", currents[0], 1)
            self.write_to_file("/pv"+filename_extension+"a2", currents[1], 1)
            self.write_to_file("/pv"+filename_extension+"a3", currents[2], 1)
            log.MainLogger().info('PV Watt: ' + str(power))
            log.MainLogger().info('PV Export: ' + str(counter))
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")


class InverterValueStoreBroker(ValueStore):
    def __init__(self, num) -> None:
        self.num = num
        self.type = "pv"
        super().__init__()

    def set(self, power: float, counter: float, currents: List[float]):
        try:
            self.is_error_set = False
            self.pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/power", power, 2)
            self.pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/counter", counter, 3)
            self.pub_to_broker("openWB/set/pv/"+str(self.num)+"/get/currents", currents, 1)
            self.reset_error()
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul store")
