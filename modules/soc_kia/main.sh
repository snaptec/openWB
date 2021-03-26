#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
socDebug=1

case $CHARGEPOINT in
	2)
		# second charge point
		socupdatetimefile="$RAMDISKDIR/kiasoctime1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		manualSocFile="$RAMDISKDIR/kiasoc1"
		socFile="$RAMDISKDIR/soc1"
		kia_email=$soc2user
		kia_password=$soc2pass
		kia_pin=$soc2pin
		kia_vin=$soc2vin
		kia_intervall=$soc2intervall
		soccalc=$kia_soccalclp2
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		manualMeterFile="$RAMDISKDIR/kia_meter_lp2"
		meterFile="$RAMDISKDIR/llkwhs1"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		socupdatetimefile="$RAMDISKDIR/kiasoctime"
		soctimerfile="$RAMDISKDIR/soctimer"
		manualSocFile="$RAMDISKDIR/kiasoc"
		socFile="$RAMDISKDIR/soc"
		kia_email=$soc_bluelink_email
		kia_password=$soc_bluelink_password
		kia_pin=$soc_bluelink_pin
		kia_vin=$soc_vin
		kia_intervall=$soc_bluelink_interval
		soccalc=$kia_soccalclp1
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		manualMeterFile="$RAMDISKDIR/kia_meter_lp1"
		meterFile="$RAMDISKDIR/llkwh"
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimervalue=$(<$soctimerfile)
tmpintervall=$(( kia_intervall * 6 ))

socDebugLog "SoCtimer: $soctimervalue, SoCIntervall: $tmpintervall"

if (( soctimervalue < tmpintervall )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	soctimervalue=$((soctimervalue+1))
	echo $soctimervalue > $soctimerfile
	if ((soccalc == 1)); then
		socDebugLog "Manual Calculation on"

		if [[ -f "$meterFile" ]]; then
			currentMeter=$(<$meterFile)
			socDebugLog "currentMeter: $currentMeter"

			# read manual Soc
			if [[ -f "$manualSocFile" ]]; then
				manualSoc=$(<$manualSocFile)
			else
				# set manualSoc to 0 as a starting point
				manualSoc=0
				echo $manualSoc > $manualSocFile
			fi
			socDebugLog "manual SoC: $manualSoc"

			# read manualMeterFile if file exists and manualMeterFile is newer than manualSocFile
			if [[ -f "$manualMeterFile" ]] && [ "$manualMeterFile" -nt "$manualSocFile" ]; then
				manualMeter=$(<$manualMeterFile)
			else
				# manualMeterFile does not exist or is outdated
				# update manualMeter with currentMeter
				manualMeter=$currentMeter
				echo $manualMeter > $manualMeterFile
			fi
			socDebugLog "manualMeter: $manualMeter"

			# read current soc
			if [[ -f "$socFile" ]]; then
				currentSoc=$(<$socFile)
			else
				currentSoc=$manualSoc
				echo $currentSoc > $socFile
			fi
			socDebugLog "currentSoc: $currentSoc"

			# calculate newSoc
			currentMeterDiff=$(echo "scale=5;$currentMeter - $manualMeter" | bc)
			socDebugLog "currentMeterDiff: $currentMeterDiff"
			currentEffectiveMeterDiff=$(echo "scale=5;$currentMeterDiff * $efficiency / 100" | bc)
			socDebugLog "currentEffectiveMeterDiff: $currentEffectiveMeterDiff ($efficiency %)"
			currentSocDiff=$(echo "scale=5;100 / $akkug * $currentEffectiveMeterDiff" | bc)
			socDebugLog "currentSocDiff: $currentSocDiff"
			newSoc=$(echo "scale=0;($manualSoc + $currentSocDiff) / 1" | bc)
			if (( newSoc > 100 )); then
				newSoc=100
			fi
			if (( newSoc < 0 )); then
				newSoc=0
			fi
			socDebugLog "newSoc: $newSoc"
			echo $newSoc > $socFile
		else
			# no current meter value for calculation -> Exit
			socDebugLog "ERROR: no meter value for calculation! ($meterFile)"
		fi
	fi
else
	socDebugLog "Requesting SoC"
	echo 0 > $soctimerfile
	sudo python3 $MODULEDIR/kiasoc.py $kia_email $kia_password $kia_pin $kia_vin $manualSocFile $socupdatetimefile >> $LOGFILE
	if ((soccalc == 0)); then
		socDebugLog "Manual Calculation off - Applying Online SoC"
		soc=$(<$manualSocFile)
		echo $soc > $socFile
	fi
fi
