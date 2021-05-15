#!/bin/bash

python /var/www/html/openWB/modules/wr2_huawei/huawei.py $pv2ip $pv2id
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt

