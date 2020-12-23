#!/bin/bash
  
python /var/www/html/openWB/modules/bezug_solaX/solaX.py $bezug1_ip

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
