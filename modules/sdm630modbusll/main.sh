#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#auch für SDM230 nutzbar (L2 und L3 bleiben dann immer 0
#ll = ladeleistung soll Modbus ID 1 sein

lla1=$(curl -s localhost:8080/last/1 |jq '.Current.L1' | tr -d '\n' | sed 's/\..*$//')
lla2=$(curl -s localhost:8080/last/1 |jq '.Current.L2' | tr -d '\n' | sed 's/\..*$//')
lla3=$(curl -s localhost:8080/last/1 |jq '.Current.L3' | tr -d '\n' | sed 's/\..*$//')
ladeleistung=`curl -s localhost:8080/last/1 |jq '.Power.L1' | tr -d '\n' | sed 's/\..*$//'`


echo $ladeleistung > /var/www/html/openWB/ramdisk/llaktuell
echo $lla1 > /var/www/html/openWB/ramdisk/lla1
echo $lla2 > /var/www/html/openWB/ramdisk/lla2
echo $lla3 > /var/www/html/openWB/ramdisk/lla3

wattbezugint=0
