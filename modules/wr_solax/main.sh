#!/bin/bash
  
python /var/www/html/openWB/modules/wr_solax/solax.py $bezug1_ip


pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
