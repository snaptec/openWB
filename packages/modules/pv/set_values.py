import os
from pathlib import Path

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
        values: [power,
                counter, (in Watt)
                [current1, current2, current3]]
        """
        try:
            if ramdisk == True:
                self.write_to_ramdisk(values)
            else:
                self.pub_to_broker(num, values)
        except Exception as e:
            log.log_exception_comp(e, ramdisk)

    def write_to_ramdisk(self, values):
        try:
            values[0] = [round(val, 1) for val in values[0]]
            self.write_to_file("/pvwatt", int(values[0]))
            self.write_to_file("/pvkwh", round(values[1], 3))
            self.write_to_file("/pvkwhk", round(values[1]/1000, 3))
            self.write_to_file("/pva1", round(values[2][0], 1))
            self.write_to_file("/pva2", round(values[2][1], 1))
            self.write_to_file("/pva3", round(values[2][2], 1))
            # if int(os.environ.get('debug')) >= 1:
            #     log.log_1_9('PV Watt: ' + str(int(values[0])))
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
            pub.pub("openWB/set/pv/"+str(num)+"/get/power", round(values[0], 2))
            pub.pub("openWB/set/pv/"+str(num)+"/get/counter", round(values[1], 3))
            values[2] = [round(val, 1) for val in values[2]]
            pub.pub("openWB/set/pv/"+str(num)+"/get/current", values[2])
        except Exception as e:
            log.log_exception_comp(e, False)
