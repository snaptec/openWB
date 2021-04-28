#!/bin/bash

#sudo python /var/www/html/openWB/modules/wr_studer/studer_wr.py $studer_ip $studer_xt $studer_vc $studer_vc_type
sudo python /var/www/html/openWB/modules/wr_studer/studer_wr.py 192.168.178.155 2 2 VS

# Rückgabe des Wertes Gesamt-PV-Leistung
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt



