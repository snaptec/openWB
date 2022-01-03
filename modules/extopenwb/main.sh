#!/bin/bash
chargep=$1
ip=$2
chargepcp=$3
outputname="extopenwb"$chargep"temp"
timeout 1 mosquitto_sub -v -h $ip -t openWB/lp/$chargepcp/# > /var/www/html/openWB/ramdisk/$outputname
myipaddress=$(</var/www/html/openWB/ramdisk/ipaddress)
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

if [[ $(wc -l </var/www/html/openWB/ramdisk/$outputname) -ge 5 ]]; then

	watt=$(grep \/W /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	VPhase1=$(grep VPhase1 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	VPhase2=$(grep VPhase2 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	VPhase3=$(grep VPhase3 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	APhase1=$(grep APhase1 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	APhase2=$(grep APhase2 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	APhase3=$(grep APhase3 /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}')
	boolChargeStat=$(grep boolChargeStat /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	boolPlugStat=$(grep boolPlugStat /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}') 
	kWhCounter=$(grep kWhCounter /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}')
	LastScannedRfidTag=$(grep LastScannedRfidTag /var/www/html/openWB/ramdisk/$outputname |head -1 | awk '{print $2}')

	if (( chargep == "1" ));then
		echo $VPhase1 > /var/www/html/openWB/ramdisk/llv1
		echo $VPhase2 > /var/www/html/openWB/ramdisk/llv2
		echo $VPhase3 > /var/www/html/openWB/ramdisk/llv3
		echo $APhase1 > /var/www/html/openWB/ramdisk/lla1
		echo $APhase2 > /var/www/html/openWB/ramdisk/lla2
		echo $APhase3 > /var/www/html/openWB/ramdisk/lla3
		echo $watt > /var/www/html/openWB/ramdisk/llaktuell
		echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwh
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstat
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestat
		soc=$(</var/www/html/openWB/ramdisk/soc)
		mosquitto_pub -h $ip -r -t openWB/set/lp/$chargepcp/%Soc -m "$soc"
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
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstats1
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestats1
		soc=$(</var/www/html/openWB/ramdisk/soc1)
		mosquitto_pub -h $ip -r -t openWB/set/lp/$chargepcp/%Soc -m "$soc"
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
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstatlp3
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestatlp3
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
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstatlp$chargep
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestatlp$chargep
	fi
	if ! [ -z $LastScannedRfidTag ] && [ $LastScannedRfidTag -ge "3" ]; then
		echo $LastScannedRfidTag > /var/www/html/openWB/ramdisk/readtag
		mosquitto_pub -h $ip -r -t openWB/set/isss/ClearRfid -m "1"
	fi

	mosquitto_pub -h $ip -r -t openWB/set/isss/parentWB -m "$myipaddress"
	if (( chargepcp == "1" )); then
		mosquitto_pub -h $ip -r -t openWB/set/isss/parentCPlp1 -m "$chargep"
	else
		mosquitto_pub -h $ip -r -t openWB/set/isss/parentCPlp2 -m "$chargep"
	fi
	mosquitto_pub -h $ip -r -t openWB/set/isss/heartbeat -m "0"
	openwbModulePublishState "LP" 0 "Kein Fehler" $chargep
	echo 0 > /var/www/html/openWB/ramdisk/errcounterextopenwb
else
	openwbModulePublishState "LP" 1 "Keine Daten vom LP erhalten, IP Korrekt?" $chargep
	openwbDebugLog "MAIN" 0 "Keine Daten von externe openWB LP $chargep empfangen"
	errcounter=$(</var/www/html/openWB/ramdisk/errcounterextopenwb)
	errcounter=$((errcounter+1))
	echo $errcounter > /var/www/html/openWB/ramdisk/errcounterextopenwb
	if (( errcounter > 5 )); then
		echo "Fehler bei Auslesung externe openWB LP $chargep, Netzwerk oder Konfiguration prüfen" > /var/www/html/openWB/ramdisk/lastregelungaktiv
	fi
fi
