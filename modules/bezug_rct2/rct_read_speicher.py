#!/usr/bin/python3
import os
import sys
import time
from typing import List
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebündelt ab


# Entry point with parameter check
def main(argv: List[str]):
    start_time = time.time()
    rct_lib.init(argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        try:
            MyTab = []
            socx    = rct_lib.add_by_name(MyTab, 'battery.soc')
            watt1   = rct_lib.add_by_name(MyTab, 'g_sync.p_acc_lp')
            watt2   = rct_lib.add_by_name(MyTab, 'battery.stored_energy')
            watt3   = rct_lib.add_by_name(MyTab, 'battery.used_energy')
            stat1   = rct_lib.add_by_name(MyTab, 'battery.bat_status')
            stat2   = rct_lib.add_by_name(MyTab, 'battery.status')
            stat3   = rct_lib.add_by_name(MyTab, 'battery.status2')
            socsoll = rct_lib.add_by_name(MyTab, 'battery.soc_target')

            # read all parameters
            response = rct_lib.read(clientsocket, MyTab)
            rct_lib.close(clientsocket)

            # output all response elements
            rct_lib.dbglog("Overall access time: {:.3f} seconds".format(time.time() - start_time))
            rct_lib.dbglog(rct_lib.format_list(response))
        except Exception as e:
            rct_lib.close(clientsocket)
            raise(e)

        # postprocess values
        socx    = socx.value
        watt1   = int(watt1.value) * -1.0
        watt2   = int(watt2.value)
        watt3   = int(watt3.value)
        stat1   = int(stat1.value)
        stat2   = int(stat2.value)
        stat3   = int(stat3.value)
        socsoll = int(socsoll.value * 100.0)


        soc = int(socx * 100.0)
        rct_lib.write_ramdisk('speichersoc', soc, '0x959930BF battery.soc')
        rct_lib.write_ramdisk('speicherleistung', watt1, '0x400F015B g_sync.p_acc_lp')
        rct_lib.write_ramdisk('speicherikwh', watt2, '0x5570401B battery.stored_energy')
        rct_lib.write_ramdisk('speicherekwh', watt3, '#0xA9033880 battery.used_energy')

        if (stat1 + stat2 + stat3) > 0:
            faultStr = "Battery ALARM Battery-Status nicht 0"
            faultState = 2
            # speicher in mqtt
        else:
            faultStr = ''
            faultState = 0

        os.system('mosquitto_pub -r -t openWB/set/housebattery/faultState -m "' + str(faultState) + '"')
        os.system('mosquitto_pub -r -t openWB/set/housebattery/faultStr -m "' + str(faultStr) + '"')
        os.system('mosquitto_pub -r -t openWB/housebattery/soctarget -m "' + str(socsoll) + '"')


if __name__ == "__main__":
    main(sys.argv[1:])