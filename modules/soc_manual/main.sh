#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_manual: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

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

incrementTimer(){
	case $dspeed in
		1)
			# Regelgeschwindigkeit 10 Sekunden
			ticksize=1
			;;
		2)
			# Regelgeschwindigkeit 20 Sekunden
			ticksize=2
			;;
		3)
			# Regelgeschwindigkeit 60 Sekunden
			ticksize=1
			;;
		*)
			# Regelgeschwindigkeit unbekannt
			ticksize=1
			;;
	esac
	soctimer=$((soctimer+$ticksize))
	echo $soctimer > $soctimerfile
}

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"

if (( soctimer < socIntervall )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Calculating manual SoC"
	# reset timer
	echo 0 > $soctimerfile

	# read current meter
	if [[ -f "$meterFile" ]]; then
		currentMeter=$(<$meterFile)
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: currentMeter: $currentMeter"

		# read manual Soc
		if [[ -f "$manualSocFile" ]]; then
			manualSoc=$(<$manualSocFile)
		else
			# set manualSoc to 0 as a starting point
			manualSoc=0
			echo $manualSoc > $manualSocFile
		fi
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: manual SoC: $manualSoc"

		# read manualMeterFile if file exists and manualMeterFile is newer than manualSocFile
		if [[ -f "$manualMeterFile" ]] && [ "$manualMeterFile" -nt "$manualSocFile" ]; then
			manualMeter=$(<$manualMeterFile)
		else
			# manualMeterFile does not exist or is outdated
			# update manualMeter with currentMeter
			manualMeter=$currentMeter
			echo $manualMeter > $manualMeterFile
		fi
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: manualMeter: $manualMeter"

		# read current soc
		if [[ -f "$socFile" ]]; then
			currentSoc=$(<$socFile)
		else
			currentSoc=$manualSoc
			echo $currentSoc > $socFile
		fi
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: currentSoc: $currentSoc"

		# calculate newSoc
		currentMeterDiff=$(echo "scale=5;$currentMeter - $manualMeter" | bc)
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: currentMeterDiff: $currentMeterDiff"
		currentEffectiveMeterDiff=$(echo "scale=5;$currentMeterDiff * $efficiency / 100" | bc)
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: currentEffectiveMeterDiff: $currentEffectiveMeterDiff ($efficiency %)"
		currentSocDiff=$(echo "scale=5;100 / $akkug * $currentEffectiveMeterDiff" | bc | awk '{printf"%d\n",$1}')
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: currentSocDiff: $currentSocDiff"
		newSoc=$(echo "$manualSoc + $currentSocDiff" | bc)
		if (( newSoc > 100 )); then
			newSoc=100
		fi
		if (( newSoc < 0 )); then
			newSoc=0
		fi
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: newSoc: $newSoc"
		echo $newSoc > $socFile
	else
		# no current meter value for calculation -> Exit
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: ERROR: no meter value for calculation! ($meterFile)"
	fi
fi

openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: --- Manual SoC end ---"
