#!/usr/bin/python3
import sys
import rct_lib
import time

# Author Heinz Hoefling
# Version 1.0 Okt.2021

def find(id, tab):
    for l in tab:
        if l.id == id:
            return l.value
    return null    

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
            
            print( "Battery Controler    : " + str(rct_lib.host) )
            Version = find(0x1B39A3A3, MyTab)
            print( "Hardware Version     : " + str(Version))
            Version = find(0x9D785E8C, MyTab) 
            print( "Software Version     : " + str(Version) )
            Ser = find(0x16A1F844, MyTab) 
            print( "Serial Nr            : " + str(Ser) )

            Status =  find(0x70A2AF4F, MyTab) 
            print( "Status               : "  + str(Status) )
            cap =  find(0xB57B59BD, MyTab) 
            print( "Max.Lade/Enladetrom A: "  + str(cap) + ' A' )
            cyl =  find(0xC0DF2978, MyTab) 
            print( "Durchlaufene Zyklen  : "  + str(cyl) )
            Eff =  (find(0xACF7666B, MyTab) * 10000) / 100.0
            print( "Efficency            : "  + str(Eff) + ' %' )
            Soh =  find(0x381B8BF9, MyTab) 
            print( "SoH                  : "  + str(Soh) )
            SoC =  int(find(0x959930BF, MyTab) *10000) / 100
            print( "SoC                  : "  + str(SoC) + ' %' )

            temp =  int(find(0x55DDF7BA, MyTab) * 100) / 100.0
            print( "Max Cell Temp.       : "  + str(temp) + ' Grad' )

            ms1  =  str(find(0xFBF6D834, MyTab))
            if  str(ms1)>"  ":
                print( "Batt.Pack 1 SN       : "  + str(ms1) )
            ms2  =  str(find(0x99396810, MyTab))
            if  str(ms2)>"  ":
                print( "Batt.Pack 2 SN       : "  + str(ms2) )
            ms3  =  str(find(0x73489528, MyTab))
            if  str(ms3)>"  ":
                print( "Batt.Pack 3 SN       : "  + str(ms3) )
            ms4  =  str(find(0x257B7612, MyTab))
            if  str(ms4)>"  ":
                print( "Batt.Pack 4 SN       : "  + str(ms4) )
            ms5  =  str(find(0x4E699086, MyTab))
            if  str(ms5)>"  ":
                print( "Batt.Pack 5 SN       : "  + str(ms5) )
            ms6  =  str(find(0x162491E8, MyTab))
            if  ms6>"  ":
                print( "Batt.Pack 6 SN       : "  + str(ms6) )


            Stat1=  find(0x71765BD8, MyTab)
            print( "Batt Status 1        : "  + str(Stat1) )
            Stat2=  find(0x0DE3D20D, MyTab)
            print(  "Batt Status 2        : "  + str(Stat2) )

            Stor=  (int(find(0x5570401B, MyTab)) / 1000.0)
            print(  "Gespeicherte Energy  : "  + str(Stor) + ' Kwh' )
            Used=  (int(find(0xA9033880, MyTab)) / 1000.0)
            print(  "Entnommene Energy    : "  + str(Used) + ' Kwh' )
        
        
        except Exception as e:
            rct_lib.close(clientsocket)
            raise(e)
            
    sys.exit(0)

if __name__ == "__main__":
    main()
