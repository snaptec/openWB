#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/studer.py "${studer_ip}" "${studer_xt}" "${studer_vc}" "${studer_vc_type}"

# Rückgabe des Wertes Gesamt-PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
