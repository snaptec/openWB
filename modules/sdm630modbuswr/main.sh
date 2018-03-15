#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#auch für SDM230 nutzbar (L2 und L3 bleiben dann immer 0
#wrwatt = Wattleistung Wechselrichter soll Modbus ID 3 sein

wra1=$(curl -s localhost:8080/last/3 |jq '.Current.L1' | tr -d '\n' | sed 's/\..*$//')
wra2=$(curl -s localhost:8080/last/3 |jq '.Current.L2' | tr -d '\n' | sed 's/\..*$//')
wra3=$(curl -s localhost:8080/last/3 |jq '.Current.L3' | tr -d '\n' | sed 's/\..*$//')
wrwatt=`curl -s localhost:8080/last/3 |jq '.Power.L1' | tr -d '\n' | sed 's/\..*$//'`


echo $wrwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $wra1 > /var/www/html/openWB/ramdisk/wra1
echo $wra2 > /var/www/html/openWB/ramdisk/wra2
echo $wra3 > /var/www/html/openWB/ramdisk/wra3

