#!/bin/bash
python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_bezug.py --ip=$bezug1_ip
#
# Nehme wattbezug als ergbenis mit zurueck da beim Bezug-Module ein Returnwert erwartet wird.
#  
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
