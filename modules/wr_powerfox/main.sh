#!/bin/bash
output=$(curl --connect-timeout 3 -s -u $powerfoxuser:"$powerfoxpass" "https://backend.powerfox.energy/api/2.0/my/$powerfoxpvid/current")

bezugwh=$(echo $output | jq '.A_Plus')
echo $bezugwh > /var/www/html/openWB/ramdisk/pvkwh

watt=$(echo $output | jq '.Watt')
echo $watt > /var/www/html/openWB/ramdisk/pvwatt

echo $watt
