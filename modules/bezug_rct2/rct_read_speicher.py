#!/usr/bin/python
import os
import sys
import rct
import fnmatch
#
# Author Heinz Hoefling
# Version 1.0 Okt.2021
# Fragt die Werte gebuendelt ab, 
#

def writeRam(fn,val, rctname):
    fnn = "/var/www/html/openWB/ramdisk/"+str(fn)
    if rct.bVerbose == True:
        f = open(fnn,'r')
        oldv = f.read()
        f.close()
        rct.dbglog("field " + str(fnn)+ " val is "+ str(val) + " oldval:"+ str(oldv) + " "  + str(rctname) )
    
    f = open(fnn,'w')
    f.write(str(val))
    f.close()
    

# Entry point with parameter check
def main():
    rct.init(sys.argv)

    clientsocket = rct.connect_to_server()
    if clientsocket is not None:

        soc =int(rct.read(clientsocket,0x959930BF ) * 100.0)
        writeRam('speichersoc', soc, '0x959930BF battery.soc')

        watt =int(rct.read(clientsocket,0x400F015B ) * -1.0 ) 
        writeRam('speicherleistung', watt, '0x400F015B g_sync.p_acc_lp')

        watt =int(rct.read(clientsocket,0x5570401B ))
        #rct.dbglog("speicherikwh will be battery.stored_energy "+ str(watt)) 
        writeRam('speicherikwh', watt, '0x5570401B battery.stored_energy')

        watt =int(rct.read(clientsocket,0xA9033880 ))
        #rct.dbglog("speicherekwh will be battery.used_energy "+ str(watt))         
        writeRam('speicherekwh', watt, '#0xA9033880 battery.used_energy')

        stat1 = int(rct.read(clientsocket,0x70A2AF4F ))
        rct.dbglog("battery.bat_status "+ str(stat1))

        stat2 = int(rct.read(clientsocket,0x71765BD8 ))
        rct.dbglog("battery.status "+ str(stat2))

        stat3 = int(rct.read(clientsocket,0x0DE3D20D ))
        rct.dbglog("battery.status2 "+ str(stat3))
        
        faultStr=''
        faultState=0

        if ( stat1 + stat2 + stat3) > 0:
            faultStr = "Battery ALARM Battery-Status nicht 0"
            faultState=2
             # speicher in mqtt 
           
        os.system('mosquitto_pub -r -t openWB/housebattery/faultState -m "' + str(faultState) +'"')
        os.system('mosquitto_pub -r -t openWB/housebattery/faultStr -m "' + str(faultStr) +'"')
   
        rct.close(clientsocket)
    sys.exit(0)
    
if __name__ == "__main__":
    main()
