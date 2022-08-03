#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

chargep=$1
ip=$2
chargepcp=$3
outputname="$RAMDISKDIR/extopenwb${chargep}temp"
timeout 1 mosquitto_sub -v -h "$ip" -t "openWB/lp/$chargepcp/#" > "$outputname"
myipaddress=$(<"$RAMDISKDIR/ipaddress")

if [[ $(wc -l <"$outputname") -ge 5 ]]; then

	watt=$(grep "\/W" "$outputname" |head -1 | awk '{print $2}') 
	VPhase1=$(grep "VPhase1" "$outputname" |head -1 | awk '{print $2}') 
	VPhase2=$(grep "VPhase2" "$outputname" |head -1 | awk '{print $2}') 
	VPhase3=$(grep "VPhase3" "$outputname" |head -1 | awk '{print $2}') 
	APhase1=$(grep "APhase1" "$outputname" |head -1 | awk '{print $2}')
	APhase2=$(grep "APhase2" "$outputname" |head -1 | awk '{print $2}') 
	APhase3=$(grep "APhase3" "$outputname" |head -1 | awk '{print $2}')
	boolChargeStat=$(grep "boolChargeStat" "$outputname" |head -1 | awk '{print $2}') 
	boolPlugStat=$(grep "boolPlugStat" "$outputname" |head -1 | awk '{print $2}') 
	kWhCounter=$(grep "kWhCounter" "$outputname" |head -1 | awk '{print $2}')
	LastScannedRfidTag=$(grep "LastScannedRfidTag" "$outputname" |head -1 | awk '{print $2}')

	if (( chargep == "1" ));then
		echo "$VPhase1" > "$RAMDISKDIR/llv1"
		echo "$VPhase2" > "$RAMDISKDIR/llv2"
		echo "$VPhase3" > "$RAMDISKDIR/llv3"
		echo "$APhase1" > "$RAMDISKDIR/lla1"
		echo "$APhase2" > "$RAMDISKDIR/lla2"
		echo "$APhase3" > "$RAMDISKDIR/lla3"
		echo "$watt" > "$RAMDISKDIR/llaktuell"
		echo "$kWhCounter" > "$RAMDISKDIR/llkwh"
		echo "$boolPlugStat" > "$RAMDISKDIR/plugstat"
		echo "$boolChargeStat" > "$RAMDISKDIR/chargestat"
		soc=$(<"$RAMDISKDIR/soc")
		mosquitto_pub -h "$ip" -r -t "openWB/set/lp/$chargepcp/%Soc" -m "$soc"
	fi
	if (( chargep == "2" ));then
		echo "$VPhase1" > "$RAMDISKDIR/llvs11"
		echo "$VPhase2" > "$RAMDISKDIR/llvs12"
		echo "$VPhase3" > "$RAMDISKDIR/llvs13"
		echo "$APhase1" > "$RAMDISKDIR/llas11"
		echo "$APhase2" > "$RAMDISKDIR/llas12"
		echo "$APhase3" > "$RAMDISKDIR/llas13"
		echo "$watt" > "$RAMDISKDIR/llaktuells1"
		echo "$kWhCounter" > "$RAMDISKDIR/llkwhs1"
		echo "$boolPlugStat" > "$RAMDISKDIR/plugstats1"
		echo "$boolChargeStat" > "$RAMDISKDIR/chargestats1"
		soc=$(<"$RAMDISKDIR/soc1")
		mosquitto_pub -h "$ip" -r -t "openWB/set/lp/$chargepcp/%Soc" -m "$soc"
	fi
	if (( chargep == "3" ));then
		echo "$VPhase1" > "$RAMDISKDIR/llvs21"
		echo "$VPhase2" > "$RAMDISKDIR/llvs22"
		echo "$VPhase3" > "$RAMDISKDIR/llvs23"
		echo "$APhase1" > "$RAMDISKDIR/llas21"
		echo "$APhase2" > "$RAMDISKDIR/llas22"
		echo "$APhase3" > "$RAMDISKDIR/llas23"
		echo "$watt" > "$RAMDISKDIR/llaktuells2"
		echo "$kWhCounter" > "$RAMDISKDIR/llkwhs2"
		echo "$boolPlugStat" > "$RAMDISKDIR/plugstatlp3"
		echo "$boolChargeStat" > "$RAMDISKDIR/chargestatlp3"
	fi
	if (( chargep > "3" ));then
		echo "$VPhase1" > "$RAMDISKDIR/llv1lp$chargep"
		echo "$VPhase2" > "$RAMDISKDIR/llv2lp$chargep"
		echo "$VPhase3" > "$RAMDISKDIR/llv3lp$chargep"
		echo "$APhase1" > "$RAMDISKDIR/lla1lp$chargep"
		echo "$APhase2" > "$RAMDISKDIR/lla2lp$chargep"
		echo "$APhase3" > "$RAMDISKDIR/lla3lp$chargep"
		echo "$watt" > "$RAMDISKDIR/llaktuelllp$chargep"
		echo "$kWhCounter" > "$RAMDISKDIR/llkwhlp$chargep"
		echo "$boolPlugStat" > "$RAMDISKDIR/plugstatlp$chargep"
		echo "$boolChargeStat" > "$RAMDISKDIR/chargestatlp$chargep"
	fi
	if [ -n "$LastScannedRfidTag" ] && [ "$LastScannedRfidTag" -ge "3" ]; then
		echo "$LastScannedRfidTag" > "$RAMDISKDIR/readtag"
		mosquitto_pub -h "$ip" -r -t "openWB/set/isss/ClearRfid" -m "1"
	fi

	mosquitto_pub -h "$ip" -r -t "openWB/set/isss/parentWB" -m "$myipaddress"
	if (( chargepcp == "1" )); then
		mosquitto_pub -h "$ip" -r -t "openWB/set/isss/parentCPlp1" -m "$chargep"
	else
		mosquitto_pub -h "$ip" -r -t "openWB/set/isss/parentCPlp2" -m "$chargep"
	fi
	mosquitto_pub -h "$ip" -r -t "openWB/set/isss/heartbeat" -m "0"
	openwbModulePublishState "LP" 0 "Kein Fehler" "$chargep"
	echo 0 > "$RAMDISKDIR/errcounterextopenwb"
else
	openwbModulePublishState "LP" 1 "Keine Daten vom LP erhalten, IP Korrekt?" "$chargep"
	openwbDebugLog "MAIN" 0 "Keine Daten von externe openWB LP $chargep empfangen"
	errcounter=$(<"$RAMDISKDIR/errcounterextopenwb")
	errcounter=$(( errcounter + 1 ))
	echo "$errcounter" > "$RAMDISKDIR/errcounterextopenwb"
	if (( errcounter > 5 )); then
		echo "Fehler bei Auslesung externe openWB LP $chargep, Netzwerk und Konfiguration prüfen" > "$RAMDISKDIR/lastregelungaktiv"
	fi
fi
