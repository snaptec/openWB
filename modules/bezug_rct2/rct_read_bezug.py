#!/usr/bin/python3
import os
import sys
from bezug_rct2 import rct_lib
from typing import List


# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebuendelt ab, nicht mit einer Connection je Wert
#
# Schreib und logge einen Wert in die Ramdisk
#


def writeRam(fn, val, rctname):
    fnn = "/var/www/html/openWB/ramdisk/"+str(fn)
    if rct_lib.bVerbose == True:
        f = open(fnn, 'r')
        oldv = f.read()
        f.close()
        rct_lib.dbglog("field " + str(fnn) + " val is:" + str(val) + " oldval:" + str(oldv) + " " + str(rctname))
    f = open(fnn, 'w')
    f.write(str(val))
    f.close()

#
# Entry point with parameter check
#


def main(argv: List[str]):
    rct_lib.init(argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        #
        # read all values in one connection to rct

        totalfeed = int(rct_lib.read(clientsocket, 0x44D4C533)*-1.0)
        #rct_lib.dbglog("einspeisungkwh is "+ str(totalfeed))
        writeRam('einspeisungkwh', totalfeed, '0x44D4C533 energy.e_grid_feed_total')

        totalload = int(rct_lib.read(clientsocket, 0x62FBE7DC))
        #rct_lib.dbglog("bezugkwh is "+ str(totalload))
        writeRam('bezugkwh',        totalload, '#0x62FBE7DC energy.e_grid_load_total')

        value = rct_lib.read(clientsocket, 0x6002891F)
        writeRam('wattbezug', int(value)*1, '#0x6002891F g_sync.p_ac_sc_sum')

        volt1 = int(rct_lib.read(clientsocket, 0xCF053085))
        volt1 = int(volt1 * 10) / 10.0
        #rct_lib.dbglog("volt1 is "+ str(volt1))
        writeRam('evuv1', volt1, '0xCF053085 g_sync.u_l_rms[0] ')

        volt2 = int(rct_lib.read(clientsocket, 0x54B4684E))
        volt2 = int(volt2 * 10) / 10.0
        #rct_lib.dbglog("volt2 is "+ str(volt2))
        writeRam('evuv2', volt2, '0x54B4684E g_sync.u_l_rms[1] ')

        volt3 = int(rct_lib.read(clientsocket, 0x2545E22D))
        volt3 = int(volt3 * 10) / 10.0
        #rct_lib.dbglog("volt3 is "+ str(volt3))
        writeRam('evuv3', volt3, '0x2545E22D g_sync.u_l_rms[2] ')

        watt = int(rct_lib.read(clientsocket, 0x27BE51D9))
        writeRam('bezugw1', watt, '0x27BE51D9 als Watt g_sync.p_ac_sc[0]')
        ampere = int(watt / volt1 * 10.0) / 10.0
        writeRam('bezuga1', ampere, '0x27BE51D9 als Ampere g_sync.p_ac_sc[0]')

        watt = int(rct_lib.read(clientsocket, 0xF5584F90))
        writeRam('bezugw2', watt, '0xF5584F90 als Watt g_sync.p_ac_sc[1]')
        ampere = int(watt / volt2 * 10.0) / 10.0
        writeRam('bezuga2', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[1]')

        watt = int(rct_lib.read(clientsocket, 0xB221BCFA))
        writeRam('bezugw3', watt, '0xB221BCFA als Watt g_sync.p_ac_sc[2]')
        ampere = int(watt / volt3 * 10.0) / 10.0
        writeRam('bezuga3', ampere, '0xF5584F90 als Ampere g_sync.p_ac_sc[2]')

        freq = rct_lib.read(clientsocket, 0x1C4A665F)
        freq = int(freq * 100) / 100.0
        #rct_lib.dbglog("freq is "+ str(freq))
        writeRam('evuhz', freq, '0x1C4A665F grid_pll[0].f')
        writeRam('llhz', freq, '0x1C4A665F grid_pll[0].f')

        stat1 = int(rct_lib.read(clientsocket, 0x37F9D5CA))
        rct_lib.dbglog("status1 " + str(stat1))

        stat2 = int(rct_lib.read(clientsocket, 0x234B4736))
        rct_lib.dbglog("status2 " + str(stat2))

        stat3 = int(rct_lib.read(clientsocket, 0x3B7FCD47))
        rct_lib.dbglog("status3 " + str(stat3))

        stat4 = int(rct_lib.read(clientsocket, 0x7F813D73))
        rct_lib.dbglog("status4 " + str(stat4))

        faultStr = ''
        faultState = 0

        if (stat1 + stat2 + stat3 + stat4) > 0:
            faultStr = "ALARM EVU Status nicht 0"
            faultState = 2
            # speicher in mqtt

        os.system('mosquitto_pub -r -t openWB/evu/faultState -m "' + str(faultState) + '"')
        os.system('mosquitto_pub -r -t openWB/evu/faultStr -m "' + str(faultStr) + '"')

        rct_lib.close(clientsocket)
    sys.exit(0)
