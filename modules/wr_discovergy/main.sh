#!/bin/bash
. /var/www/html/openWB/openwb.conf
output=$(curl --connect-timeout 5 -s -u $discovergyuser:$discovergypass "https://api.discovergy.com/public/v1/last_reading?meterId=$discovergypvid")

pvwh=$(echo $output | jq .values.energyOut)
pvwh=$(( bezugwh / 10000000 ))
echo $bezugwh > /var/www/html/openWB/ramdisk/pvkwh

watt=$(echo $output | jq .values.power)
watt=$(( watt / 1000 ))
echo $watt > /var/www/html/openWB/ramdisk/pvwatt


echo $watt

