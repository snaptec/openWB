#!/usr/bin/python
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
        rct.dbglog("val for " + str(fnn)+ " is "+ str(val) + " "  + str(rctname) )
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

        pv1watt=int(rct.read(clientsocket,0xB5317B78 ))
        pv2watt=int(rct.read(clientsocket,0xAA9AA253 ))
        pv3watt=int(rct.read(clientsocket,0xE96F1844 )) 
        rct.dbglog("pvwatt A:"+ str(pv1watt) + "  B:"+ str(pv2watt) + " G:"+ str(pv3watt) )
        
        writeRam('pv1wattString1', int(pv1watt), 'pv1watt')
        writeRam('pv1wattString2', int(pv2watt), 'pv2watt')
        pvwatt = ( (pv1watt+pv2watt+pv3watt) * -1 )
        writeRam('pvwatt', int(pvwatt), 'negative Summe von pv1watt + pv2watt + pv3watt')

        pv1total=int(rct.read(clientsocket,0xFC724A9E ))
        pv2total=int(rct.read(clientsocket,0x68EEFD3D ))
        pv3total=int(rct.read(clientsocket,0x0F28E2E1 ))
        rct.dbglog("pvtotal  A:"+ str(pv1total) + "  B:"+ str(pv2total) + " G:"+ str(pv3total) )
        pvkwh  = (pv1total + pv2total + pv3total) 
        writeRam('pvkwh', pvkwh, 'Summe von pv1total pv1total pv1total')

        rct.close(clientsocket)
    sys.exit(0)
    
if __name__ == "__main__":
    main()
