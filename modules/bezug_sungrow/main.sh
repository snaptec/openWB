#!/bin/bash 
 
python /var/www/html/openWB/modules/bezug_sungrow/sungrow.py $speicher_ip 
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug) 
echo $wattbezug

