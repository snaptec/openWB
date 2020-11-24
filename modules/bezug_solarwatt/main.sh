#!/bin/bash



sresponse=$(curl --connect-timeout 3 -s "http://$speichersolarwattip/rest/kiwigrid/wizard/devices")

bezugwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkConsumedFromGrid.value' | sed 's/\..*$//')
echo $bezugwh > /var/www/html/openWB/ramdisk/bezugkwh
einspeisungwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkOut.value' | sed 's/\..*$//')
echo $einspeisungwh  > /var/www/html/openWB/ramdisk/einspeisungkwh

bezugw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerConsumedFromGrid.value' | sed 's/\..*$//')
einspeisungw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerOut.value' | sed 's/\..*$//')
bezugwatt=$(echo "scale=0; $bezugw - $einspeisungw /1" |bc)

echo $bezugwatt > /var/www/html/openWB/ramdisk/wattbezug

echo $bezugwatt
