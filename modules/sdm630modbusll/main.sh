#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#get modbuswerte
#curl localhost:8080/last/11 |jq ..... !rest to test!


#llVolt
#llPhase1 x Ampere
#llPhase2 x Ampere
#llPhase3 x Ampere
lla1=$(curl -s localhost:8080/last/1 |jq '.Current.L1' | tr -d '\n' | sed 's/\..*$//')
lla2=$(curl -s localhost:8080/last/1 |jq '.Current.L2' | tr -d '\n' | sed 's/\..*$//')
lla3=$(curl -s localhost:8080/last/1 |jq '.Current.L3' | tr -d '\n' | sed 's/\..*$//')
#calc :
#ladeleistung= (lla1+lla2+lla3)*llVolt
ladeleistung=`curl -s localhost:8080/last/1 |jq '.Power.L1' | tr -d '\n' | sed 's/\..*$//'`


echo $ladeleistung > /var/www/html/openWB/ramdisk/llaktuell
echo $lla1 > /var/www/html/openWB/ramdisk/lla1
echo $lla2 > /var/www/html/openWB/ramdisk/lla2
echo $lla3 > /var/www/html/openWB/ramdisk/lla3

wattbezugint=0
