#!/bin/bash
chargep=$1
ip=$2
answer=$(timeout 4 curl -s $ip/connect.php | jq .)
if [[ $answer == *"vehicle_id"* ]]; then
	watt=$(echo $answer |jq '.power_all')
	watt=$(echo $watt | sed 's/\..*$//')
	APhase1=$(echo $answer | jq ".currents[0]" ) 
	APhase2=$(echo $answer | jq ".currents[1]" ) 
	APhase3=$(echo $answer | jq ".currents[2]" ) 
	boolChargeStat=$(echo $answer | jq ".charge_state" )
	if [ $boolChargeStat = true ]; then
		boolChargeStat=1
	else
		boolChargeStat=0
	fi
	boolPlugStat=$(echo $answer | jq ".plug_state") 
	if [ $boolPlugStat = true ]; then
		boolPlugStat=1
	else
		boolPlugStat=0
	fi

	kWhCounter=$(echo $answer | jq ".imported")
	kWhCounter=$(echo "scale=3;$kWhCounter / 1000" |bc)

	if (( chargep == "1" ));then
		echo $APhase1 > /var/www/html/openWB/ramdisk/lla1
		echo $APhase2 > /var/www/html/openWB/ramdisk/lla2
		echo $APhase3 > /var/www/html/openWB/ramdisk/lla3
		echo $watt > /var/www/html/openWB/ramdisk/llaktuell
		echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwh
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstat
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestat
	fi
	if (( chargep == "2" ));then
		echo $APhase1 > /var/www/html/openWB/ramdisk/llas11
		echo $APhase2 > /var/www/html/openWB/ramdisk/llas12
		echo $APhase3 > /var/www/html/openWB/ramdisk/llas13
		echo $watt > /var/www/html/openWB/ramdisk/llaktuells1
		echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhs1
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstats1
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestats1
	fi
	if (( chargep == "3" ));then
		echo $APhase1 > /var/www/html/openWB/ramdisk/llas21
		echo $APhase2 > /var/www/html/openWB/ramdisk/llas22
		echo $APhase3 > /var/www/html/openWB/ramdisk/llas23
		echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
		echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhs2
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstatlp3
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestatlp3
	fi
	if (( chargep > "3" ));then
		echo $APhase1 > /var/www/html/openWB/ramdisk/lla1lp$chargep
		echo $APhase2 > /var/www/html/openWB/ramdisk/lla2lp$chargep
		echo $APhase3 > /var/www/html/openWB/ramdisk/lla3lp$chargep
		echo $watt > /var/www/html/openWB/ramdisk/llaktuelllp$chargep
		echo $kWhCounter > /var/www/html/openWB/ramdisk/llkwhlp$chargep
		echo $boolPlugStat > /var/www/html/openWB/ramdisk/plugstatlp$chargep
		echo $boolChargeStat > /var/www/html/openWB/ramdisk/chargestatlp$chargep
	fi

	openwbModulePublishState "LP" 0 "Kein Fehler" $chargep
	echo 0 > /var/www/html/openWB/ramdisk/errcounterowbpro
else
	openwbModulePublishState "LP" 1 "Keine Daten vom LP erhalten, IP Korrekt?" $chargep
	openwbDebugLog "MAIN" 0 "Keine Daten von openWB Pro LP $chargep empfangen"
	errcounter=$(</var/www/html/openWB/ramdisk/errcounterextopenwb)
	errcounter=$((errcounter+1))
	echo $errcounter > /var/www/html/openWB/ramdisk/errcounterextopenwb
	if (( errcounter > 5 )); then
		echo "Fehler bei Auslesung openWB Pro LP $chargep, Netzwerk oder Konfiguration prüfen" > /var/www/html/openWB/ramdisk/lastregelungaktiv
	fi
fi
