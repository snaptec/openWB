#!/usr/bin/python3
from typing import List
import os, sys, traceback, time
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebuendelt ab, nicht mit einer Connection je Wert

# Entry point with parameter check
def main(argv: List[str]):
    start_time = time.time()
    rct = rct_lib.RCT(argv)

    if rct.connect_to_server() == True:
        try:
            # generate id list for fast bulk read
            MyTab = []
            totalfeed   = rct.add_by_name(MyTab, 'energy.e_grid_feed_total')
            totalload   = rct.add_by_name(MyTab, 'energy.e_grid_load_total')
            p_ac_sc_sum = rct.add_by_name(MyTab, 'g_sync.p_ac_sc_sum')
            volt1       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[0]')
            volt2       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[1]')
            volt3       = rct.add_by_name(MyTab, 'g_sync.u_l_rms[2]')
            watt1       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[0]')
            watt2       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[1]')
            watt3       = rct.add_by_name(MyTab, 'g_sync.p_ac_sc[2]')
            freq        = rct.add_by_name(MyTab, 'grid_pll[0].f')
            stat1       = rct.add_by_name(MyTab, 'fault[0].flt')
            stat2       = rct.add_by_name(MyTab, 'fault[1].flt')
            stat3       = rct.add_by_name(MyTab, 'fault[2].flt')
            stat4       = rct.add_by_name(MyTab, 'fault[3].flt')

            # read all parameters
            response = rct.read(MyTab)
            rct.close()
            
            # postprocess values
            totalfeed   = int(totalfeed.value*-1.0)
            totalload   = int(totalload.value)
            p_ac_sc_sum = p_ac_sc_sum.value
            volt1       = int(volt1.value * 10) / 10.0
            volt2       = int(volt2.value * 10) / 10.0
            volt3       = int(volt3.value * 10) / 10.0
            watt1       = int(watt1.value)
            watt2       = int(watt2.value)
            watt3       = int(watt3.value)
            freq        = int(freq.value * 100) / 100.0
            stat1       = int(stat1.value)
            stat2       = int(stat2.value)
            stat3       = int(stat3.value)
            stat4       = int(stat4.value)

            #
            # Adjust and write values to ramdisk
            rct.write_ramdisk('einspeisungkwh', totalfeed, '0x44D4C533 energy.e_grid_feed_total')
            rct.write_ramdisk('bezugkwh',       totalload, '#0x62FBE7DC energy.e_grid_load_total')
            rct.write_ramdisk('wattbezug', int(p_ac_sc_sum)*1, '#0x6002891F g_sync.p_ac_sc_sum')
            rct.write_ramdisk('evuv1', volt1, '0xCF053085 g_sync.u_l_rms[0] ')
            rct.write_ramdisk('evuv2', volt2, '0x54B4684E g_sync.u_l_rms[1] ')
            rct.write_ramdisk('evuv3', volt3, '0x2545E22D g_sync.u_l_rms[2] ')

            rct.write_ramdisk('bezugw1', watt1, '0x27BE51D9 als Watt g_sync.p_ac_sc[0]')
            ampere = int(watt1 / volt1 * 10.0) / 10.0
            rct.write_ramdisk('bezuga1', ampere, '0x27BE51D9 als Ampere g_sync.p_ac_sc[0]')

            rct.write_ramdisk('bezugw2', watt2, '0xF5584F90 als Watt g_sync.p_ac_sc[1]')
            ampere = int(watt2 / volt2 * 10.0) / 10.0
            rct.write_ramdisk('bezuga2', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[1]')

            rct.write_ramdisk('bezugw3', watt3, '0xB221BCFA als Watt g_sync.p_ac_sc[2]')
            ampere = int(watt3 / volt3 * 10.0) / 10.0
            rct.write_ramdisk('bezuga3', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[2]')

            rct.write_ramdisk('evuhz', freq, '0x1C4A665F grid_pll[0].f')
            rct.write_ramdisk('llhz', freq, '0x1C4A665F grid_pll[0].f')

            if (stat1 + stat2 + stat3 + stat4) > 0:
                faultStr = "ALARM EVU Status nicht 0"
                faultState = 2
                # speicher in mqtt
            else:
                faultStr = ''
                faultState = 0

            os.system('mosquitto_pub -r -t openWB/set/evu/faultState -m "' + str(faultState) + '"')
            os.system('mosquitto_pub -r -t openWB/set/evu/faultStr -m "' + str(faultStr) + '"')

            # debug output of processing time and all response elements
            rct.dbglog(response.format_list(time.time() - start_time))
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None

if __name__ == "__main__":
    main(sys.argv[1:])