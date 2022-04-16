#!/usr/bin/python3
from typing import List
import os, sys, traceback, time
import rct_lib
from rct_lib import rct_id

# Author Heinz Hoefling
# Version 1.0 Okt.2021


# Entry point with parameter check
def main(argv: List[str]):
    start_time = time.time()
    rct = rct_lib.RCT(argv)

    if rct.connect_to_server() == True:
        try:
            MyTab = []
            MyTab.append(rct_id(0    ,  0,  '-----------------Batterie-------------------- '))
            rct.add_by_name(MyTab, 'battery.soc')
            rct.add_by_name(MyTab, 'battery.efficiency')
            rct.add_by_name(MyTab, 'acc_conv.i_acc_lp_fast')
            rct.add_by_name(MyTab, 'battery.current')
            rct.add_by_name(MyTab, 'battery.voltage')
            rct.add_by_name(MyTab, 'power_mng.u_acc_lp')
            rct.add_by_name(MyTab, 'power_mng.u_acc_mix_lp')
            rct.add_by_name(MyTab, 'adc.u_acc')
            rct.add_by_name(MyTab, 'g_sync.p_acc_lp')
            rct.add_by_name(MyTab, 'energy.e_dc_total[0]')
            rct.add_by_name(MyTab, 'energy.e_dc_total[1]')
            MyTab.append(rct_id(0    , 0,     '------------------- Panels A -----------------'))
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc')
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].p_dc_lp')
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[0].u_sg_lp')
            rct.add_by_name(MyTab, 'g_sync.u_sg_avg[0]')
            MyTab.append(rct_id(0    , 0,     '----------------- Panels B --------------------'))
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc')
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].p_dc_lp')
            rct.add_by_name(MyTab, 'dc_conv.dc_conv_struct[1].u_sg_lp')
            rct.add_by_name(MyTab, 'g_sync.u_sg_avg[1]')
            MyTab.append(rct_id(0         , 0,     '---------- WR/Netz/Haus Spannungen --------------'))
            rct.add_by_name(MyTab, 'g_sync.u_l_rms[0]')
            rct.add_by_name(MyTab, 'g_sync.u_l_rms[1]')
            rct.add_by_name(MyTab, 'g_sync.u_l_rms[2]')
            MyTab.append(rct_id(0         , 0,     '----------------------- WR --------------------- '))
            rct.add_by_name(MyTab, 'g_sync.i_dr_eff[0]')
            rct.add_by_name(MyTab, 'g_sync.i_dr_eff[1]')
            rct.add_by_name(MyTab, 'g_sync.i_dr_eff[2]')
            MyTab.append(rct_id(0         , 0,     '--------WR  3* U*I = Watt erzeugung des WR ------'))
            rct.add_by_name(MyTab, 'g_sync.p_ac[0]')
            rct.add_by_name(MyTab, 'g_sync.p_ac[1]')
            rct.add_by_name(MyTab, 'g_sync.p_ac[2]')
            MyTab.append(rct_id(0         , 0,     '--------------- HAUS Verbrauch --------------------'))
            rct.add_by_name(MyTab, 'g_sync.p_ac_load[0]')
            rct.add_by_name(MyTab, 'g_sync.p_ac_load[1]')
            rct.add_by_name(MyTab, 'g_sync.p_ac_load[2]')
            MyTab.append(rct_id(0         , 0,     '--------------------- Netz ------------------' ))
            rct.add_by_name(MyTab, 'g_sync.p_ac_sc[0]')
            rct.add_by_name(MyTab, 'g_sync.p_ac_sc[1]')
            rct.add_by_name(MyTab, 'g_sync.p_ac_sc[2]')
            rct.add_by_name(MyTab, 'g_sync.p_ac_grid_sum_lp')
            rct.add_by_name(MyTab, 'grid_offset')
            rct.add_by_name(MyTab, 'grid_pll[0].f')
            MyTab.append(rct_id(0         , 0,     '--------------------- ----- ------------------'))

            # read via rct_id list
            response = rct.read(MyTab)
            rct.close()

            # debug output of processing time and all response elements
            rct.dbglog(response.format_list(time.time() - start_time))
        except:
            print("-"*100)
            traceback.print_exc(file=sys.stdout)
            rct.close()

    rct = None
            
if __name__ == "__main__":
    main(sys.argv[1:])