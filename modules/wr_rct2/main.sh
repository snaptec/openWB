#!/bin/bash
   

   
python /var/www/html/openWB/modules/bezug_rct2/rct_read_wr.py --ip=$bezug1_ip
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
