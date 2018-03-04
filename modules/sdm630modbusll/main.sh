#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#get modbuswerte
curl localhost:8080/last/11 |jq ..... !rest to test!


llVolt
llPhase1 x Ampere
llPhase2 x Ampere
llPhase3 x Ampere

calc :
ladeleistung= (lla1+lla2+lla3)*llVolt


echo $ladeleistung > /var/run/llaktuell
echo $lla1 > /var/run/lla1
echo $lla2 > /var/run/lla2
echo $lla3 > /var/run/lla3

