#!/bin/bash

if [ -n "$bezug1_ip" ]; then
  opt=""
else
  echo "$0 Debughilfe bezug1_ip parameter not supplied use 192.168.208.63"
  bezug1_ip=192.168.208.63
  opt=" -v" 
  #opt=""     # Kein echo!
fi

#
# Exportere Volt/Ampere/Frequenz etc in die Ramdisk
#   

python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_bezug.py $opt --ip=$bezug1_ip

#
# Nehme wattbezug als ergbenis mit zurueck da beim Bezug-Module ein Returnwert erwartet wird.
#  
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
