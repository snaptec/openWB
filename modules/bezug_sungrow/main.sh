#!/bin/bash 

sudo python3 /var/www/html/openWB/packages/modules/counter/sungrow.py "${speicher1_ip}" "${sungrowsr}" 

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug) 
echo $wattbezug
