#!/bin/bash


#
# Exportere Volt/Ampere/Frequenz etc in die Ramdisk
#   
python /var/www/html/openWB/modules/bezug_rct2/rct_read_bezug.py --ip=$bezug1_ip
#
# Nehme wattbezug als ergbeniss mit zurück da beim Bezug-Module ein Returnwert erwartet wird.
#  
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
