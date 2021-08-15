#!/bin/bash 

python /var/www/html/openWB/modules/bezug_sungrow/sungrow.py $speicher1_ip $sungrowsr 
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug) 
echo $wattbezug
