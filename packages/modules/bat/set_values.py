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
                soc,
                [imported, exported]]
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
            self.write_to_file("/speicherleistung", int(values[0]))
            self.write_to_file("/speichersoc", int(values[1]))
            self.write_to_file("/speicherikwh", round(values[2][0], 2))
            self.write_to_file("/speicherekwh", round(values[2][1], 2))
            if int(os.environ.get('debug')) >= 1:
                log.log_1_9('BAT Watt: ' + str(int(values[0])))
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
            pub.pub("openWB/set/bat/"+str(num)+"/get/power", round(values[0], 2))
            pub.pub("openWB/set/bat/"+str(num)+"/get/soc", int(values[1]))
            pub.pub("openWB/set/bat/"+str(num)+"/get/imported", round(values[2][0], 2))
            pub.pub("openWB/set/bat/"+str(num)+"/get/exported", round(values[2][1], 2))
        except Exception as e:
            log.log_exception_comp(e, False)

