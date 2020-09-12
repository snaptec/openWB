#!/bin/bash


answer=$(curl -k --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")
evuwatt=$(echo $answer | jq -r '.site.instant_power'  | sed 's/\..*$//')
echo $evuwatt
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug
evuikwh=$(echo $answer | jq -r '.site.energy_imported')
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh
evuekwh=$(echo $answer | jq -r '.site.energy_exported')
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
