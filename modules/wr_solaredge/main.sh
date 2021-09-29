#!/bin/bash

python3 /var/www/html/openWB/packages/modules/pv/solaredge.py "${solaredgepvip}" "${solaredgepvslave1}" "${solaredgepvslave2}" "${solaredgepvslave3}" "${solaredgepvslave4}" "${wr1extprod}" "${solaredgespeicherip}" "${solaredgezweiterspeicher}" "${solaredgesubbat}" "${solaredgewr2ip}" 

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
