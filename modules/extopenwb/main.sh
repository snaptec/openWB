#!/bin/bash
chargep=$1
ip=$2
outputname="extopenwb"$chargep"temp"
timeout 1 mosquitto_sub -v -h $ip -t openWB/lp/1/# > /var/www/html/openWB/ramdisk/$outputname
#values=$(</var/www/html/openWB/ramdisk/extopenwb$chargeptemp)
#echo -e $values
#watt=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/W) 
#VPhase1=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/VPhase1) 
#VPhase2=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/VPhase2 ) 
#VPhase3=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/VPhase3 ) 
#APhase1=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/APhase1 ) 
#APhase2=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/APhase2 ) 
#APhase3=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/APhase3 ) 
#kWhCounter=$(mosquitto_sub -C 1 -h $ip -t openWB/lp/1/kWhCounter ) 


watt=$(grep 1\/W /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
VPhase1=$(grep VPhase1 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
VPhase2=$(grep VPhase2 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
VPhase3=$(grep VPhase3 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
APhase1=$(grep APhase1 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
APhase2=$(grep APhase2 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
APhase3=$(grep APhase3 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
kWhCounter=$(grep kWhCounter /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 

if (( chargep == "1" ));then
	echo $VPhase1 > /var/www/html/openWB/ramdisk/llv1
	echo $VPhase2 > /var/www/html/openWB/ramdisk/llv2
	echo $VPhase3 > /var/www/html/openWB/ramdisk/llv3
	echo $APhase1 > /var/www/html/openWB/ramdisk/lla1
	echo $APhase2 > /var/www/html/openWB/ramdisk/lla2
	echo $APhase3 > /var/www/html/openWB/ramdisk/lla3
	echo $watt > /var/www/html/openWB/ramdisk/llaktuell
	echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwh
fi
if (( chargep == "2" ));then
	echo $VPhase1 > /var/www/html/openWB/ramdisk/llvs11
	echo $VPhase2 > /var/www/html/openWB/ramdisk/llvs12
	echo $VPhase3 > /var/www/html/openWB/ramdisk/llvs13
	echo $APhase1 > /var/www/html/openWB/ramdisk/llas11
	echo $APhase2 > /var/www/html/openWB/ramdisk/llas12
	echo $APhase3 > /var/www/html/openWB/ramdisk/llas13
	echo $watt > /var/www/html/openWB/ramdisk/llaktuells1
	echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhs1
fi
if (( chargep == "3" ));then
	echo $VPhase1 > /var/www/html/openWB/ramdisk/llvs21
	echo $VPhase2 > /var/www/html/openWB/ramdisk/llvs22
	echo $VPhase3 > /var/www/html/openWB/ramdisk/llvs23
	echo $APhase1 > /var/www/html/openWB/ramdisk/llas21
	echo $APhase2 > /var/www/html/openWB/ramdisk/llas22
	echo $APhase3 > /var/www/html/openWB/ramdisk/llas23
	echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
	echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhs2
fi
if (( chargep > "3" ));then
	echo $VPhase1 > /var/www/html/openWB/ramdisk/llv1lp$chargep
	echo $VPhase2 > /var/www/html/openWB/ramdisk/llv2lp$chargep
	echo $VPhase3 > /var/www/html/openWB/ramdisk/llv3lp$chargep
	echo $APhase1 > /var/www/html/openWB/ramdisk/lla1lp$chargep
	echo $APhase2 > /var/www/html/openWB/ramdisk/lla2lp$chargep
	echo $APhase3 > /var/www/html/openWB/ramdisk/lla3lp$chargep
	echo $watt > /var/www/html/openWB/ramdisk/llaktuelllp$chargep
	echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhlp$chargep
fi

