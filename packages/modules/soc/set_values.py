import os
from pathlib import Path

try:
    from ...helpermodules import log
    from ...helpermodules import pub
    from ...helpermodules import timecheck
except:
    # for 1.9 compability
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from helpermodules import pub
    from helpermodules import timecheck


class set_values():
    def __init__(self) -> None:
        pass

    def set(self, num, values, ramdisk):
        """
        Parameter
        ---------
        values: [soc, timestamp]
        """
        try:
            if ramdisk == True:
                self.write_to_ramdisk(values)
            else:
                self.pub_to_broker(num, values)
        except Exception as e:
            log.log_exception_comp(e, ramdisk)

    def write_to_ramdisk(self, values, num):
        """
        Parameter
        ---------
        num: int
            LP-Nummer
        """
        try:
            if num == 1:
                suffix = ""
            elif num == 2:
                suffix = "1"
            if 0 < int(values[0]) <= 100:
                self.write_to_file("/soc"+suffix, int(values[0]))
            if int(os.environ.get('debug')) >= 0:
                log.log_1_9("Lp"+str(num)+": SoC: "+str(values[0]))
        except Exception as e:
            log.log_exception_comp(e, True)

    def write_to_file(self, file, value):
        try:
            with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
                f.write(str(value))
        except Exception as e:
            log.log_exception_comp(e, True)

    def pub_to_broker(self, num, values):
        """
        Parameter
        ---------
        num: int
            EV-Nummer
        """
        try:
            pub.pub("openWB/set/ev/"+str(self.num)+"/module/set/timestamp_last_request",values[1])
            pub.pub("openWB/set/pv/"+str(num)+"/get/counter", round(values[1], 3))
            values[2] = [round(val, 1) for val in values[2]]
            pub.pub("openWB/set/pv/"+str(num)+"/get/current", values[2])
        except Exception as e:
            log.log_exception_comp(e, False)

    def check_interval(self, data, plug_state, charge_state):
        """ prüft, ob das Interval zur SoC-Abfrage in Abhängigkeit von Steckerstatus und Ladestatus abgelaufen ist.

        Parameter
        ---------
        data: dict
            Modul-Konfiguration
        plug_state: bool
            Steckerstatus
        charge_state: bool
            Ladestatus
        
        Return
        ------
        bool: abfragen, nicht abfragen
        """
        try:
            request_soc = False
            if data["config"]["request_only_plugged"] == True:
                if plug_state == True:
                    if charge_state == True:
                        interval = data["config"]["request_interval_charging"]
                    else:
                        interval = data["config"]["request_interval_not_charging"]
                    # Zeitstempel prüfen, ob wieder abgefragt werden muss.
                    if "timestamp_last_request" in data["set"]:
                        if timecheck.check_timestamp(data["set"]["timestamp_last_request"], interval*60) == False:
                            # Zeit ist abgelaufen
                            request_soc = True
                    else:
                        # Initiale Abfrage
                        request_soc = True
            return request_soc
        except Exception as e:
            log.log_exception_comp(e, self.ramdisk)

    def set_state(self, ramdisk, state, str):
        """ setzt den Fehlerstatus und -text des Moduls.

        Parameter
        ---------
        ramdisk: bool
            1.9 oder 2.x
        state: int
            Fehlerstatus
        str: str
            Fehlertext
        """
        try:
            if ramdisk == True:
                pub.pub_single("openWB/set/lp/"+str(self.num)+"/socFaultState", state ,hostname="localhost", no_json=True)
                pub.pub_single("openWB/set/lp/"+str(self.num)+"/socFaultStr", str, hostname="localhost", no_json=True)
            else:
                pub.pub("openWB/set/ev/"+str(self.num)+"/module/get/fault_state", state)
                pub.pub("openWB/set/ev/"+str(self.num)+"/module/get/fault_str", str)
        except Exception as e:
            log.log_exception_comp(e, False)