#!/bin/bash

sudo python /var/www/html/openWB/modules/wr2_ethsdm120/readsdm120.py $pv2ip $pv2id $pv2ip2 $pv2id2 
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt
