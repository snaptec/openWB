#!/bin/bash

python /var/www/html/openWB/modules/wr_studer/studer_wr.py $studer_ip $studer_xt $studer_vc $studer_vc_type

# Rückgabe des Wertes Gesamt-PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
