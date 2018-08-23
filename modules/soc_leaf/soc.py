#!/usr/bin/env
import sys
import time


leaftimer = open('/var/www/html/openWB/ramdisk/soctimer', 'r')
leaftimer = int(leaftimer.read())

if ( leaftimer < 181 ):
    leaftimer += 1
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    f.write(str(leaftimer))
    f.close()

else:
    from leaf import Leaf
    leaf = Leaf(sys.argv[1], sys.argv[2])
    response = leaf.BatteryStatusCheckRequest()
    time.sleep(15)
    leaf.BatteryStatusCheckResultRequest(resultKey=response['resultKey'])
    time.sleep(10)
    socit = leaf.BatteryStatusRecordsRequest()
    justsoc = socit['BatteryStatusRecords']['BatteryStatus']['SOC']['Value']
    f = open('/var/www/html/openWB/ramdisk/soc', 'w')
    f.write(str(justsoc))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/soctimer', 'w')
    f.write(str(0))
    f.close()

    
    


