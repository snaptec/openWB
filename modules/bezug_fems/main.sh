#!/bin/bash
watt=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/ActivePower" | jq .value)
iwh=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/_sum/GridBuyActiveEnergy" | jq .value)
ewh=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/_sum/GridSellActiveEnergy" | jq .value)
evuv1=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/VoltageL1" | jq .value)
evuv2=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/VoltageL2" | jq .value)
evuv3=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/VoltageL3" | jq .value)
evua1=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/CurrentL1" | jq .value)
evua2=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/CurrentL2" | jq .value)
evua3=$(curl --connect-timeout 2 -s "http://x:$femskacopw@$femsip:8084/rest/channel/meter0/CurrentL3" | jq .value)

echo $watt > /var/www/html/openWB/ramdisk/wattbezug
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $iwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ewh > /var/www/html/openWB/ramdisk/einspeisungkwh
echo $evua1 > /var/www/html/openWB/ramdisk/bezuga1
echo $evua2 > /var/www/html/openWB/ramdisk/bezuga2
echo $evua3 > /var/www/html/openWB/ramdisk/bezuga3
echo $watt
