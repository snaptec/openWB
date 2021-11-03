#!/usr/bin/python3
import os
import sys
import rct_lib
import fnmatch

# Author Heinz Hoefling
# Version 1.0 Okt.2021

# Entry point with parameter check
def main():
    rct_lib.init(sys.argv)

    clientsocket = rct_lib.connect_to_server()
    if clientsocket is not None:                             

        print( "Battery Controler " + str(rct_lib.host) )
        Version = rct_lib.read(clientsocket, 0x1B39A3A3) 
        print( "Hardware Version     : " + str(Version))
        Version = rct_lib.read(clientsocket, 0x9D785E8C) 
        print( "Software Version     : " + str(Version) )
        Ser = rct_lib.read(clientsocket, 0x16A1F844) 
        print( "Serial Nr            : " + str(Ser[74:88]) )

        Status =  rct_lib.read(clientsocket, 0x70A2AF4F) 
        print( "Status               : "  + str(Status) )
        cap =  rct_lib.read(clientsocket, 0xB57B59BD) 
        print( "Max.Lade/Enlade      : "  + str(cap) + ' A' )
        cyl =  rct_lib.read(clientsocket, 0xC0DF2978) 
        print( "Cycles               : "  + str(cyl) )
        Eff =  int(rct_lib.read(clientsocket, 0xACF7666B) * 10000) / 100.0
        print( "Efficency            : "  + str(Eff) + ' %' )
        Soh =  rct_lib.read(clientsocket, 0x381B8BF9) 
        print( "SoH                  : "  + str(Soh) )
        SoC =  int(rct_lib.read(clientsocket, 0x959930BF) *10000) / 100
        print( "SoC                  : "  + str(SoC) + ' %' )

        temp =  int(rct_lib.read(clientsocket, 0x55DDF7BA) * 100) / 100.0
        print( "Max Cell Temp.       : "  + str(temp) + ' Grad' )

        ms1  =  rct_lib.read(clientsocket, 0xFBF6D834) 
        if ms1[75] > ".":
            print( "Batt.Pack 1          : "  + str(ms1[74:88]) )
        ms2  =  rct_lib.read(clientsocket, 0x99396810) 
        if ms2[75] > ".":
            print( "Batt.Pack 2          : "  + str(ms2[74:88]) )
        ms3  =  rct_lib.read(clientsocket, 0x73489528) 
        if ms3[75] > ".":
            print( "Batt.Pack 3          : "  + str(ms3[74:88]) )
        ms4  =  rct_lib.read(clientsocket, 0x257B7612) 
        if ms4[75] > ".":
            print( "Batt.Pack 4          : "  + str(ms4[74:88]) )
        ms5  =  rct_lib.read(clientsocket, 0x4E699086) 
        if ms5[75] > ".":
            print( "Batt.Pack 5          : "  + str(ms5[74:88]) )
        ms6  =  rct_lib.read(clientsocket, 0x162491E8) 
        if ms6[75] > '.':
            print( "Batt.Pack 6          : "  + str(ms6[74:88]) )

        Stat1=  rct_lib.read(clientsocket, 0x71765BD8)
        print( "Batt Status 1        : "  + str(Stat1) )
        Stat2=  rct_lib.read(clientsocket, 0x0DE3D20D)
        print(  "Batt Status 2        : "  + str(Stat2) )

        Stor=  (int(rct_lib.read(clientsocket, 0x5570401B)) / 1000.0)
        print( "Stored Energy        : "  + str(Stor) + ' Kwh' )
        Used=  (int(rct_lib.read(clientsocket, 0xA9033880)) / 1000.0)
        print( "Used Energy          : "  + str(Used) + ' Kwh' )

#0x902AFAFB battery.temperature                              22.8020839691
#0x65EED11B battery.voltage                                  319.721984863
#0x4B51A539 battery.prog_sn                                  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
#0x8B9FF008 battery.soc_target                               0.97000002861
#0xB84A38AB battery.soc_target_high                          0.97000002861
#0xA616B022 battery.soc_target_low                           0.97000002861
#0x4E04DD55 battery.soc_update_since                         0.188000202179
#0xA6C4FD4A battery.stack_cycles[0]                          8
#0x0CFA8BC4 battery.stack_cycles[1]                          8
#0x5BA122A5 battery.stack_cycles[2]                          8
#0x89B25F4B battery.stack_cycles[3]                          8
#0x5A9EEFF0 battery.stack_cycles[4]                          0
#0x2A30A97E battery.stack_cycles[5]                          0
#0x27C39CEA battery.stack_cycles[6]                          0
#0x6388556C battery.stack_software_version[0]                5185
#0xA54C4685 battery.stack_software_version[1]                5185
#0xC8BA1729 battery.stack_software_version[2]                5185
#0x086C75B0 battery.stack_software_version[3]                5185
#0xA40906BF battery.stack_software_version[4]                0
#0xEEA3F59B battery.stack_software_version[5]                0
#0x6974798A battery.stack_software_version[6]                0
        
        rct_lib.close(clientsocket)
    sys.exit(0)
    
if __name__ == "__main__":
    main()
