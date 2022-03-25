#!/usr/bin/python3
import sys
import rct_lib
import time

# Entry point with parameter check
def main():
    start_time =  time.time()
    rct_lib.init(sys.argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        try:
            MyTab = []
            pv1watt  = rct_lib.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc')
            pv2watt  = rct_lib.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc')
            pv3watt  = rct_lib.add_by_name(MyTab, 'io_board.s0_external_power')
            dA       = rct_lib.add_by_name(MyTab, 'energy.e_dc_day[0]')
            dB       = rct_lib.add_by_name(MyTab, 'energy.e_dc_day[1]')
            dE       = rct_lib.add_by_name(MyTab, 'energy.e_ext_day')
            mA       = rct_lib.add_by_name(MyTab, 'energy.e_dc_month[0]')
            mB       = rct_lib.add_by_name(MyTab, 'energy.e_dc_month[1]')
            mE       = rct_lib.add_by_name(MyTab, 'energy.e_ext_month')
            yA       = rct_lib.add_by_name(MyTab, 'energy.e_dc_year[0]')
            yB       = rct_lib.add_by_name(MyTab, 'energy.e_dc_year[1]')
            yE       = rct_lib.add_by_name(MyTab, 'energy.e_ext_year')
            pv1total = rct_lib.add_by_name(MyTab, 'energy.e_dc_total[0]')
            pv2total = rct_lib.add_by_name(MyTab, 'energy.e_dc_total[1]')
            pv3total = rct_lib.add_by_name(MyTab, 'energy.e_ext_total')

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
        pv1watt  = int(pv1watt.value)
        pv2watt  = int(pv2watt.value)
        pv3watt  = int(pv3watt.value)
        dA       = int(dA.value)
        dB       = int(dB.value)
        dE       = int(dE.value)
        mA       = int(mA.value)
        mB       = int(mB.value)
        mE       = int(mE.value)
        yA       = int(yA.value)
        yB       = int(yB.value)
        yE       = int(yE.value)
        pv1total = int(pv1total.value)
        pv2total = int(pv2total.value)
        pv3total = int(pv3total.value)

        # aktuell
        rct_lib.write_ramdisk('pv1wattString1', int(pv1watt), 'pv1watt')
        rct_lib.write_ramdisk('pv1wattString2', int(pv2watt), 'pv2watt')
        pvwatt = ((pv1watt+pv2watt+pv3watt) * -1)
        rct_lib.write_ramdisk('pvwatt', int(pvwatt), 'negative Summe von pv1watt + pv2watt + pv3watt')

        # daily
        daily_pvkwhk = (dA + dB + dE) / 1000.0   # -> KW
        rct_lib.write_ramdisk('daily_pvkwhk', daily_pvkwhk, 'daily_pvkwhk')

        # monthly
        monthly_pvkwhk = (mA + mB + mE) / 1000.0   # -> KW
        rct_lib.write_ramdisk('monthly_pvkwhk', monthly_pvkwhk, 'monthly_pvkwhk')

        # yearly
        yearly_pvkwhk = (yA + yB + yE) / 1000.0   # -> KW
        rct_lib.write_ramdisk('yearly_pvkwhk', yearly_pvkwhk, 'yearly_pvkwhk')

        # total
        pvkwh = (pv1total + pv2total + pv3total)
        rct_lib.write_ramdisk('pvkwh', pvkwh, 'Summe von pv1total pv1total pv1total')

    sys.exit(0)

if __name__ == "__main__":
    main()
