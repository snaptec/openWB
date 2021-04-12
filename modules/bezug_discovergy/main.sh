#!/bin/bash
output=$(curl --connect-timeout 3 -s -u $discovergyuser:"$discovergypass" "https://api.discovergy.com/public/v1/last_reading?meterId=$discovergyevuid")

einspeisungwh=$(echo $output | jq .values.energyOut)
einspeisungwh=$(( einspeisungwh / 10000000 ))
echo $einspeisungwh > /var/www/html/openWB/ramdisk/einspeisungkwh

bezugwh=$(echo $output | jq .values.energy)
bezugwh=$(( bezugwh / 10000000 ))
echo $bezugwh > /var/www/html/openWB/ramdisk/bezugkwh

vl1=$(echo $output | jq .values.voltage1)
vl1=$(( vl1 / 1000 ))
echo $vl1 > /var/www/html/openWB/ramdisk/evuv1
vl2=$(echo $output | jq .values.voltage2)
vl2=$(( vl2 / 1000 ))
echo $vl2 > /var/www/html/openWB/ramdisk/evuv2
vl3=$(echo $output | jq .values.voltage3)
vl3=$(( vl3 / 1000 ))
echo $vl3 > /var/www/html/openWB/ramdisk/evuv3
watt=$(echo $output | jq .values.power)
watt=$(( watt / 1000 ))
echo $watt > /var/www/html/openWB/ramdisk/wattbezug
wattl1=$(echo $output | jq .values.power1)
wattl1=$(( wattl1 / 1000 ))
echo $wattl1 > /var/www/html/openWB/ramdisk/bezugw1
wattl2=$(echo $output | jq .values.power2)
wattl2=$(( wattl2 / 1000 ))
echo $wattl2 > /var/www/html/openWB/ramdisk/bezugw2
wattl3=$(echo $output | jq .values.power3)
wattl3=$(( wattl3 / 1000 ))
echo $wattl3 > /var/www/html/openWB/ramdisk/bezugw3
if (( vl1 > 150 )); then
	al1=$(( wattl1 / vl1 ))
else
	al1=$(( wattl1 / 230 ))
fi
echo $al1 > /var/www/html/openWB/ramdisk/bezuga1 
if (( vl2 > 150 )); then 
	al2=$(( wattl2 / vl2 )) 
else 
	al2=$(( wattl2 / 230 )) 
fi 
echo $al2 > /var/www/html/openWB/ramdisk/bezuga2 
if (( vl3 > 150 )); then 
	al3=$(( wattl3 / vl3 )) 
else 
	al3=$(( wattl3 / 230 )) 
fi 
echo $al3 > /var/www/html/openWB/ramdisk/bezuga3
echo $watt

