#!/usr/bin/python3
import sys
from bezug_rct2 import rct_lib
from typing import List


def writeRam(fn, val, rctname):
    fnn = "/var/www/html/openWB/ramdisk/"+str(fn)
    if rct_lib.bVerbose == True:
        rct_lib.dbglog("val for " + str(fnn) + " is " + str(val) + " " + str(rctname))
        f = open(fnn, 'r')
        oldv = f.read()
        f.close()
        rct_lib.dbglog("field " + str(fnn) + " val is " + str(val) + " oldval:" + str(oldv) + " " + str(rctname))

    f = open(fnn, 'w')
    f.write(str(val))
    f.close()

# Entry point with parameter check


def main(argv: List[str]):
    rct_lib.init(argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:

        # aktuell
        pv1watt = int(rct_lib.read(clientsocket, 0xB5317B78))
        pv2watt = int(rct_lib.read(clientsocket, 0xAA9AA253))
        pv3watt = int(rct_lib.read(clientsocket, 0xE96F1844))
        rct_lib.dbglog("pvwatt A:" + str(pv1watt) + "  B:" + str(pv2watt) + " G:" + str(pv3watt))
        writeRam('pv1wattString1', int(pv1watt), 'pv1watt')
        writeRam('pv1wattString2', int(pv2watt), 'pv2watt')
        pvwatt = ((pv1watt+pv2watt+pv3watt) * -1)
        writeRam('pvwatt', int(pvwatt), 'negative Summe von pv1watt + pv2watt + pv3watt')

        # monthly
        mA = int(rct_lib.read(clientsocket, 0x81AE960B))  # energy.e_dc_month[0]  WH
        mB = int(rct_lib.read(clientsocket, 0x7AB9B045))  # energy.e_dc_month[1]  WH
        mE = int(rct_lib.read(clientsocket, 0x031A6110))  # energy.e_ext_month    WH
        monthly_pvkwhk = (mA + mB + mE) / 1000.0   # -> KW
        writeRam('monthly_pvkwhk', monthly_pvkwhk, 'monthly_pvkwhk')

        # yearly
        yA = int(rct_lib.read(clientsocket, 0xAF64D0FE))  # energy.e_dc_total[0]  WH
        yB = int(rct_lib.read(clientsocket, 0xBD55D796))  # energy.e_dc_total[1]  WH
        yE = int(rct_lib.read(clientsocket, 0xA59C8428))  # energy.e_ext_total    WH
        yearly_pvkwhk = (yA + yB + yE) / 1000.0   # -> KW
        writeRam('yearly_pvkwhk', yearly_pvkwhk, 'yearly_pvkwhk')

        # total
        pv1total = int(rct_lib.read(clientsocket, 0xFC724A9E))    # energy.e_dc_total[0]
        pv2total = int(rct_lib.read(clientsocket, 0x68EEFD3D))    # energy.e_dc_total[1]
        pv3total = int(rct_lib.read(clientsocket, 0xA59C8428))    # energy.e_ext_total
        rct_lib.dbglog("pvtotal  A:" + str(pv1total) + "  B:" + str(pv2total) + " G:" + str(pv3total))
        pvkwh = (pv1total + pv2total + pv3total)
        writeRam('pvkwh', pvkwh, 'Summe von pv1total pv1total pv1total')

# mqttvar["pv/CounterTillStartPvCharging"]=pvcounter
# mqttvar["pv/bool70PVDynStatus"]=nurpv70dynstatus
# mqttvar["pv/WhCounter"]=pvallwh
# mqttvar["pv/DailyYieldKwh"]=daily_pvkwhk
# mqttvar["pv/MonthlyYieldKwh"]=monthly_pvkwhk
# mqttvar["pv/YearlyYieldKwh"]=yearly_pvkwhk
# mqttvar["pv/1/W"]=pv1watt
# mqttvar["pv/1/WhCounter"]=pvkwh
# mqttvar["pv/1/DailyYieldKwh"]=daily_pvkwhk1
# mqttvar["pv/1/MonthlyYieldKwh"]=monthly_pvkwhk1
# mqttvar["pv/1/YearlyYieldKwh"]=yearly_pvkwhk1
# mqttvar["pv/2/W"]=pv2watt
# mqttvar["pv/2/WhCounter"]=pv2kwh
# mqttvar["pv/2/DailyYieldKwh"]=daily_pvkwhk2
# mqttvar["pv/2/MonthlyYieldKwh"]=monthly_pvkwhk2
# mqttvar["pv/2/YearlyYieldKwh"]=yearly_pvkwhk2

        rct_lib.close(clientsocket)
    sys.exit(0)

