#!/bin/bash

#DMOD="MAIN"
DMOD="PV"
Debug=$debug

python3 /var/www/html/openWB/modules/wr_solarlog/solarlog.py "${bezug_solarlog_ip}"
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 

openwbDebugLog ${DMOD} 2 "pvwatt: $pvwatt"
openwbDebugLog ${DMOD} 2 "pvkwh: $pvkwh"
echo $pvwatt
