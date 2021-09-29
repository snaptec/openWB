#!/bin/bash
python3 /var/www/html/openWB/packages/modules/counter/kostal_smart_energy_meter.py "${ksemip}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
