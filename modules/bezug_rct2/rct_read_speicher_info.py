#!/usr/bin/python3
import sys
import rct_lib
import time

# Author Heinz Hoefling
# Version 1.0 Okt.2021

# Entry point with parameter check
def main():
    start_time = time.time()
    rct_lib.init(sys.argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:
        try:
            # generate id list for fast bulk read
            MyTab = []
            rct_lib.add_by_name(MyTab, 'battery.bms_power_version')
            rct_lib.add_by_name(MyTab, "battery.bms_software_version")
            rct_lib.add_by_name(MyTab, "battery.bms_sn")
            rct_lib.add_by_name(MyTab, "battery.bat_status") 
            rct_lib.add_by_name(MyTab, "battery.ah_capacity") 
            rct_lib.add_by_name(MyTab, "battery.cycles")
            rct_lib.add_by_name(MyTab, "battery.efficiency")
            rct_lib.add_by_name(MyTab, "battery.soh")
            rct_lib.add_by_name(MyTab, "battery.soc") 
            rct_lib.add_by_name(MyTab, "battery.max_cell_temperature") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[0]")
            rct_lib.add_by_name(MyTab, "battery.module_sn[1]") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[2]")
            rct_lib.add_by_name(MyTab, "battery.module_sn[3]") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[4]") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[5]") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[6]") 
            rct_lib.add_by_name(MyTab, "battery.status")
            rct_lib.add_by_name(MyTab, "battery.status2") 
            rct_lib.add_by_name(MyTab, "battery.stored_energy") 
            rct_lib.add_by_name(MyTab, "battery.used_energy")
            rct_lib.add_by_name(MyTab, "battery.temperature")
            rct_lib.add_by_name(MyTab, "battery.voltage")
            rct_lib.add_by_name(MyTab, "battery.prog_sn")
            rct_lib.add_by_name(MyTab, "battery.soc_target")
            rct_lib.add_by_name(MyTab, "battery.soc_target_high")
            rct_lib.add_by_name(MyTab, "battery.soc_target_low")
            rct_lib.add_by_name(MyTab, "battery.soc_update_since")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[0]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[1]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[2]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[3]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[4]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[5]")
            rct_lib.add_by_name(MyTab, "battery.stack_cycles[6]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[0]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[1]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[2]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[3]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[4]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[5]")
            rct_lib.add_by_name(MyTab, "battery.stack_software_version[6]")

            # read parameters
            response = rct_lib.read(clientsocket, MyTab)
            rct_lib.close(clientsocket)
            
            # output all response elements
            rct_lib.dbglog("Overall access time: {:.3f} seconds".format(time.time() - start_time))
            rct_lib.dbglog(rct_lib.format_list(response))
        except Exception as e:
            rct_lib.close(clientsocket)
            raise(e)
            
    sys.exit(0)

if __name__ == "__main__":
    main()