from datetime import datetime, timezone
import os
from pathlib import Path
import traceback

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

class set_values():
    def __init__(self) -> None:
        pass

    def set(self, num, values, ramdisk):
        """
        Parameter
        ---------
        values: [[voltage1, voltage2, voltage3],
                [current1, current2, current3],
                counter,
                power,
                plug_state,
                charge_state]
        """
        try:
            if ramdisk == True:
                self.write_to_ramdisk(num, values)
            else:
                self.pub_to_broker(num, values)
        except Exception as e:
            log.log_exception_comp(e, ramdisk)

    def write_to_ramdisk(self, num, values):
        try:
            values[0] = [round(val, 1) for val in values[0]]
            values[1] = [round(val, 1) for val in values[1]]
            values[2] = round(values[2], 3)
            values[3] = int(values[3])
            if num <= 3:
                if num == 1:
                    suffix = ""
                elif num == 2:
                    suffix = "s1"
                    suffix2 = "lp2"
                elif num == 2:
                    suffix = "s2"
                    suffix2 = "lp3"
                self.write_to_file("/llv"+suffix+"1", values[0][0])
                self.write_to_file("/llv"+suffix+"2", values[0][1])
                self.write_to_file("/llv"+suffix+"3", values[0][2])
                self.write_to_file("/lla"+suffix+"1", values[1][0])
                self.write_to_file("/lla"+suffix+"2", values[1][1])
                self.write_to_file("/lla"+suffix+"3", values[1][2])
                self.write_to_file("/llkwh"+suffix, values[2], 3)
                self.write_to_file("/llaktuell"+suffix, values[3])
                self.write_to_file("/ladeleistung"+suffix2, values[3])
                self.write_to_file("/plugstat"+suffix, values[4])
                self.write_to_file("/chargestat"+suffix, values[5])
                if num == 3:
                    self.write_to_file("/plugstat"+suffix2, values[4])
                    self.write_to_file("/chargestat"+suffix2, values[5])
            if num > 3:
                suffix = "lp"+str(num)
                self.write_to_file("/llv1"+suffix, values[0][0])
                self.write_to_file("/llv2"+suffix, values[0][1])
                self.write_to_file("/llv3"+suffix, values[0][2])
                self.write_to_file("/lla1"+suffix, values[1][0])
                self.write_to_file("/lla2"+suffix, values[1][1])
                self.write_to_file("/lla3"+suffix, values[1][2])
                self.write_to_file("/llkwh"+suffix, values[2])
                self.write_to_file("/llaktuell"+suffix, values[3])
                self.write_to_file("/ladeleistung"+suffix, values[3])
                self.write_to_file("/plugstat"+suffix, values[4])
                self.write_to_file("/chargestat"+suffix, values[5])
            if int(os.environ.get('debug')) >= 1:
                log.log_1_9('CP Ladeleistung: ' + str(int(values[3])))
                log.log_1_9('CP Steckerstatus: ' + str(int(values[4])))
                log.log_1_9('CP Ladestatus: ' + str(int(values[5])))
        except Exception as e:
            log.log_exception_comp(e, True)

    def write_to_file(self, file, value):
        try:
            with open("/var/www/html/openWB/ramdisk/" + file, "w") as f:
                    f.write(str(value))
        except Exception as e:
            log.log_exception_comp(e, True)

    def pub_to_broker(self, num, values):
        try:
            # Format
            for n in range(len(values)):
                if isinstance(values[n], list) == True:
                    for m in range(len(values[n])):
                        values[n][m] = round(values[n][m], 2)
                else:
                    values[n] = round(values[n], 2)
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/voltage", values[0])
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/current", values[1])
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/counter", values[2])
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/power", values[3])
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/plug_state", values[4])
            pub.pub("openWB/set/chargepoint/"+str(num)+"/get/charge_state", values[5])
        except Exception as e:
            log.log_exception_comp(e, False)

