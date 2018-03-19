#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#auch für SDM230 nutzbar (L2 und L3 bleiben dann immer 0
#bezug = bezug soll Modbus ID 2 sein
. /var/www/html/openWB/openwb.conf

#check ob gonium reader lauft
if ps ax |grep -v grep |grep "sdm630_httpd-linux-arm -s $sdm630modbusbezugsource -d SDM:$sdm630modbusbezugid -u $sdm630modbusbezugport" > /dev/null
then
else 
		sudo /home/pi/bin/sdm630_httpd-linux-arm -s $sdm630modbusbezugsource -d SDM:$sdm630modbusbezugid -u $sdm630modbusbezugport &
fi
	
bezuga1=$(curl -s localhost:8080/last/$sdm630modbusbezugid |jq '.Current.L1' | tr -d '\n' | sed 's/\..*$//')
bezuga2=$(curl -s localhost:8080/last/$sdm630modbusbezugid |jq '.Current.L2' | tr -d '\n' | sed 's/\..*$//')
bezuga3=$(curl -s localhost:8080/last/$sdm630modbusbezugid |jq '.Current.L3' | tr -d '\n' | sed 's/\..*$//')
wattbezug=`curl -s localhost:8080/last/$sdm630modbusbezugid |jq '.Power.L1' | tr -d '\n' | sed 's/\..*$//'`


echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3

