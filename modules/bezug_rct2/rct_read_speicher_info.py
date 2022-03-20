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

        print( "Battery Controler    : " + str(rct_lib.host) )
        Version = rct_lib.read(clientsocket, 0x1B39A3A3) 
        print( "Hardware Version     : " + str(Version))
        Version = rct_lib.read(clientsocket, 0x9D785E8C) 
        print( "Software Version     : " + str(Version) )
        Ser = rct_lib.read(clientsocket, 0x16A1F844) 
        print( "Serial Nr            : " + str(Ser[74:88]) )

        Status =  rct_lib.read(clientsocket, 0x70A2AF4F) 
        print( "Status               : "  + str(Status) )
        cap =  rct_lib.read(clientsocket, 0xB57B59BD) 
        print( "Max.Lade/Enladetrom A: "  + str(cap) + ' A' )
        cyl =  rct_lib.read(clientsocket, 0xC0DF2978) 
        print( "Durchlaufene Zyklen  : "  + str(cyl) )
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
            print( "Batt.Pack 1 SN       : "  + str(ms1[74:88]) )
        ms2  =  rct_lib.read(clientsocket, 0x99396810) 
        if ms2[75] > ".":
            print( "Batt.Pack 2 SN       : "  + str(ms2[74:88]) )
        ms3  =  rct_lib.read(clientsocket, 0x73489528) 
        if ms3[75] > ".":
            print( "Batt.Pack 3 SN       : "  + str(ms3[74:88]) )
        ms4  =  rct_lib.read(clientsocket, 0x257B7612) 
        if ms4[75] > ".":
            print( "Batt.Pack 4 SN       : "  + str(ms4[74:88]) )
        ms5  =  rct_lib.read(clientsocket, 0x4E699086) 
        if ms5[75] > ".":
            print( "Batt.Pack 5 SN       : "  + str(ms5[74:88]) )
        ms6  =  rct_lib.read(clientsocket, 0x162491E8) 
        if ms6[75] > '.':
            print( "Batt.Pack 6 SN       : "  + str(ms6[74:88]) )

        Stat1=  rct_lib.read(clientsocket, 0x71765BD8)
        print( "Batt Status 1        : "  + str(Stat1) )
        Stat2=  rct_lib.read(clientsocket, 0x0DE3D20D)
        print(  "Batt Status 2        : "  + str(Stat2) )

        Stor=  (int(rct_lib.read(clientsocket, 0x5570401B)) / 1000.0)
        print(  "Gespeicherte Energy  : "  + str(Stor) + ' Kwh' )
        Used=  (int(rct_lib.read(clientsocket, 0xA9033880)) / 1000.0)
        print(  "Entnommene Energy    : "  + str(Used) + ' Kwh' )
        
        rct_lib.close(clientsocket)
    else:
        print( "Battery Controler " + str(rct_lib.host) + " not availble" )
    sys.exit(0)
    
if __name__ == "__main__":
    main()
