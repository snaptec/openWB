#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#get modbuswerte
#curl localhost:8080/last/11 |jq ..... !rest to test!


#llVolt
#llPhase1 x Ampere
#llPhase2 x Ampere
#llPhase3 x Ampere
lla1=0
lla2=0
lla3=0
#calc :
#ladeleistung= (lla1+lla2+lla3)*llVolt
ladeleistung=0

echo $ladeleistung > /var/www/html/openWB/ramdisk/llaktuell
echo $lla1 > /var/www/html/openWB/ramdisk/lla1
echo $lla2 > /var/www/html/openWB/ramdisk/lla2
echo $lla3 > /var/www/html/openWB/ramdisk/lla3

