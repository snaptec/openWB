#!/bin/bash

sudo python /var/www/html/openWB/modules/wr2_solaredge/solaredge.py $pv2ip $pv2id
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt
