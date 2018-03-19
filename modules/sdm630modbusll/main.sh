#!/bin/bash

###############
#SDM630v2 wird mithilfe von https://github.com/gonium/gosdm630 ausgelesen.
#auch für SDM230 nutzbar (L2 und L3 bleiben dann immer 0
#ll = ladeleistung soll Modbus ID 1 sein
# Gonium Tool fragt standard nur ID1 ab

. /var/www/html/openWB/openwb.conf


if [[ $sdm630modbusllsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm630modbusllsource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
	sudo socat pty,link=$sdm630modbusllsource,raw tcp:$sdm630modbuslllanip:26
	fi
else
	echo "echo" > /dev/null
fi


#check ob gonium reader lauft
if ps ax |grep -v grep |grep "sdm630_httpd-linux-arm -s $sdm630modbusllsource -d SDM:$sdm630modbusllid -u $sdm630modbusllport" > /dev/null 
then
	echo "test" > /dev/null
else 
	sudo /home/pi/bin/sdm630_httpd-linux-arm -s $sdm630modbusllsource -d SDM:$sdm630modbusllid -u $sdm630modbusllport &
fi


lla1=$(curl -s localhost:8080/last/$sdm630modbusllid |jq '.Current.L1' | tr -d '\n' | sed 's/\..*$//')
lla2=$(curl -s localhost:8080/last/$sdm630modbusllid |jq '.Current.L2' | tr -d '\n' | sed 's/\..*$//')
lla3=$(curl -s localhost:8080/last/$sdm630modbusllid |jq '.Current.L3' | tr -d '\n' | sed 's/\..*$//')
ladeleistung=`curl -s localhost:8080/last/$sdm630modbusllid |jq '.Power.L1' | tr -d '\n' | sed 's/\..*$//'`


echo $ladeleistung > /var/www/html/openWB/ramdisk/llaktuell
echo $lla1 > /var/www/html/openWB/ramdisk/lla1
echo $lla2 > /var/www/html/openWB/ramdisk/lla2
echo $lla3 > /var/www/html/openWB/ramdisk/lla3

wattbezugint=0
