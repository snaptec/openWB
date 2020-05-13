#!/bin/bash

soc=$(curl -s -u $bydhvuser:$bydhvpass http://$bydhvip/asp/RunData.asp | grep -A 2 SOC: | sed -n 2p | cut -f1 -d"%" | sed 's/.*value=//')
echo $soc > /var/www/html/openWB/ramdisk/speichersoc
speicherleistung=$(curl -s -u $bydhvuser:$bydhvpass http://$bydhvip/asp/Home.asp | grep -A 2 Power: | sed -n 2p | sed 's/.*value=//' | cut -f1 -d">")
speicherleistung=$(echo "($speicherleistung*1000)/1" |bc)
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung
