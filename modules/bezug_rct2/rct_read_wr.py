#!/usr/bin/python3
from bezug_rct2 import rct_lib
from typing import List


def writeRam(fn, val, rctname):
    fnn = "/var/www/html/openWB/ramdisk/"+str(fn)
    if rct_lib.bVerbose:
        rct_lib.dbglog("val for " + str(fnn) + " is " + str(val) + " " + str(rctname))
        with open(fnn, 'r') as f:
            oldv = f.read()
        rct_lib.dbglog("field " + str(fnn) + " val is " + str(val) + " oldval:" + str(oldv) + " " + str(rctname))

    with open(fnn, 'w') as f:
        f.write(str(val))


# Entry point with parameter check
def main(argv: List[str]):
    rct_lib.init(argv[0])

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

        rct_lib.close(clientsocket)
