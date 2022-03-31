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
            HWVersion = rct_lib.add_by_name(MyTab, 'battery.bms_power_version')
            SWVersion = rct_lib.add_by_name(MyTab, "battery.bms_software_version")
            Ser       = rct_lib.add_by_name(MyTab, "battery.bms_sn")
            Status    = rct_lib.add_by_name(MyTab, "battery.bat_status") 
            cap       = rct_lib.add_by_name(MyTab, "battery.ah_capacity") 
            cycl      = rct_lib.add_by_name(MyTab, "battery.cycles")
            Eff       = rct_lib.add_by_name(MyTab, "battery.efficiency")
            Soh       = rct_lib.add_by_name(MyTab, "battery.soh")
            SoC       = rct_lib.add_by_name(MyTab, "battery.soc") 
            temp      = rct_lib.add_by_name(MyTab, "battery.max_cell_temperature") 
            ms1       = rct_lib.add_by_name(MyTab, "battery.module_sn[0]")
            ms2       = rct_lib.add_by_name(MyTab, "battery.module_sn[1]") 
            ms3       = rct_lib.add_by_name(MyTab, "battery.module_sn[2]")
            ms4       = rct_lib.add_by_name(MyTab, "battery.module_sn[3]") 
            ms5       = rct_lib.add_by_name(MyTab, "battery.module_sn[4]") 
            ms6       = rct_lib.add_by_name(MyTab, "battery.module_sn[5]") 
            rct_lib.add_by_name(MyTab, "battery.module_sn[6]") 
            Stat1     = rct_lib.add_by_name(MyTab, "battery.status")
            Stat2     = rct_lib.add_by_name(MyTab, "battery.status2") 
            Stor      = rct_lib.add_by_name(MyTab, "battery.stored_energy") 
            Used      = rct_lib.add_by_name(MyTab, "battery.used_energy")
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

            print( "Battery Controller   : " + str(rct_lib.host) )
            print( "Hardware Version     : " + str(HWVersion.value))
            print( "Software Version     : " + str(SWVersion.value) )
            print( "Serial Nr            : " + str(Ser.value) )
            print( "Status               : "  + str(Status.value) )
            print( "Max.Lade/Enladetrom A: "  + str(cap.value) + ' A' )
            print( "Durchlaufene Zyklen  : "  + str(cycl.value) )
            Eff =  (Eff.value * 10000) / 100.0
            print( "Efficency            : "  + str(Eff) + ' %' )
            print( "SoH                  : "  + str(Soh.value) )
            SoC =  int(SoC.value *10000) / 100
            print( "SoC                  : "  + str(SoC) + ' %' )
            temp =  int(temp.value * 100) / 100.0
            print( "Max Cell Temp.       : "  + str(temp) + ' Grad' )

            if  str(ms1.value)>"  ":
                print( "Batt.Pack 1 SN       : "  + str(ms1.value) )
            if  str(ms2.value)>"  ":
                print( "Batt.Pack 2 SN       : "  + str(ms2.value) )
            if  str(ms3.value)>"  ":
                print( "Batt.Pack 3 SN       : "  + str(ms3.value) )
            if  str(ms4.value)>"  ":
                print( "Batt.Pack 4 SN       : "  + str(ms4.value) )
            if  str(ms5.value)>"  ":
                print( "Batt.Pack 5 SN       : "  + str(ms5.value) )
            if  str(ms6.value)>"  ":
                print( "Batt.Pack 6 SN       : "  + str(ms6.value) )


            print( "Batt Status 1        : "  + str(Stat1.value) )
            print( "Batt Status 2        : "  + str(Stat2.value) )
            Stor=  (int(Stor.value) / 1000.0)
            print(  "Gespeicherte Energy  : "  + str(Stor) + ' Kwh' )
            Used=  (int(Used.value) / 1000.0)
            print(  "Entnommene Energy    : "  + str(Used) + ' Kwh' )

        except Exception as e:
            rct_lib.close(clientsocket)
            raise(e)
            
    sys.exit(0)

if __name__ == "__main__":
    main()