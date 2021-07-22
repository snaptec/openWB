#!/bin/bash

sudo python /var/www/html/openWB/modules/wr_ethsdm120/readsdm120.py $wr_sdm120ip $wr_sdm120id 
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
