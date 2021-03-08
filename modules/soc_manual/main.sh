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
		manualSocFile="$RAMDISKDIR/manual_soc_lp2"
		manualMeterFile="$RAMDISKDIR/manual_soc_meter_lp2"
		socFile="$RAMDISKDIR/soc1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		socIntervall=1 # update every minute if script is called every 10 seconds
		meterFile="$RAMDISKDIR/llkwhs1"
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		manualSocFile="$RAMDISKDIR/manual_soc_lp1"
		manualMeterFile="$RAMDISKDIR/manual_soc_meter_lp1"
		socFile="$RAMDISKDIR/soc"
		soctimerfile="$RAMDISKDIR/soctimer"
		socIntervall=1 # update every minute if script is called every 10 seconds
		meterFile="$RAMDISKDIR/llkwh"
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

incrementTimer(){
	soctimer=$((soctimer+1))
	echo $soctimer > $soctimerfile
}

soctimer=$(<$soctimerfile)

if (( soctimer < socIntervall )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	incrementTimer
else
	socDebugLog "Calculating manual SoC"
	# reset timer
	echo 0 > $soctimerfile

	# read current meter
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
		currentSocDiff=$(echo "scale=5;100 / $akkug * $currentEffectiveMeterDiff" | bc | sed 's/\..*$//')
		socDebugLog "currentSocDiff: $currentSocDiff"
		newSoc=$(echo "$manualSoc + $currentSocDiff" | bc)
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

socDebugLog "--- Manual SoC end ---"
