#!/bin/bash
output=$(curl --connect-timeout 3 -s -u $powerfoxuser:"$powerfoxpass" "https://backend.powerfox.energy/api/2.0/my/$powerfoxid/current")

einspeisungwh=$(echo $output | jq '.A_Minus')
echo $einspeisungwh > /var/www/html/openWB/ramdisk/einspeisungkwh

bezugwh=$(echo $output | jq '.A_Plus')
echo $bezugwh > /var/www/html/openWB/ramdisk/bezugkwh

watt=$(echo $output | jq '.Watt')
echo $watt > /var/www/html/openWB/ramdisk/wattbezug

echo $watt
