#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
# socDebug=1

case $CHARGEPOINT in
	2)
		# second charge point
		socsuccessfile="$RAMDISKDIR/socsuccess1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		manualSocFile="$RAMDISKDIR/bluelinksoc1"
		socFile="$RAMDISKDIR/soc1"
		bluelink_email=$soc2user
		bluelink_password=$soc2pass
		bluelink_pin=$soc2pin
		bluelink_vin=$soc2vin
		bluelink_intervall=$soc2intervall
		soccalc=$kia_soccalclp2
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		manualMeterFile="$RAMDISKDIR/bluelink_meter_lp2"
		meterFile="$RAMDISKDIR/llkwhs1"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		socsuccessfile="$RAMDISKDIR/socsuccess"
		soctimerfile="$RAMDISKDIR/soctimer"
		manualSocFile="$RAMDISKDIR/bluelinksoc"
		socFile="$RAMDISKDIR/soc"
		bluelink_email=$soc_bluelink_email
		bluelink_password=$soc_bluelink_password
		bluelink_pin=$soc_bluelink_pin
		bluelink_vin=$soc_vin
		bluelink_intervall=$soc_bluelink_interval
		soccalc=$kia_soccalclp1
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		manualMeterFile="$RAMDISKDIR/bluelink_meter_lp1"
		meterFile="$RAMDISKDIR/llkwh"
		;;
esac

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
		ticksize=6
		;;
	*)
		# Regelgeschwindigkeit unbekannt
		ticksize=1
		;;
esac

socDebugLog(){
	if (( socDebug >= $1 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: LP$CHARGEPOINT: $2" >> $LOGFILE
	fi
}

socDebugLog 1 "-----------------------------------------------------------"
socDebugLog 1 "Bluelink SoC Module starting"

soctimervalue=$(<$soctimerfile)
tmpintervall=$(( bluelink_intervall * 6 ))
ticksLeft=$((tmpintervall - soctimervalue))
timeLeft=$(echo "scale=1;$ticksLeft / 6" | bc | sed 's/^\./0./')
socDebugLog 1 "    Next update: $timeLeft minutes ($ticksLeft ticks)"

if (( soctimervalue < tmpintervall )); then
	
	soctimervalue=$((soctimervalue+ticksize))
	echo $soctimervalue > $soctimerfile

	if ((soccalc == 0)); then
		socDebugLog 1 "    Nothing to do yet"	
	fi

	if ((soccalc == 1)); then
		socDebugLog 1 "    Manual Calculation starting"

		if [[ -f "$meterFile" ]]; then
			currentMeter=$(<$meterFile)

			# read manual Soc
			if [[ -f "$manualSocFile" ]]; then
				manualSoc=$(<$manualSocFile)
			else
				# set manualSoc to 0 as a starting point
				manualSoc=0
				echo $manualSoc > $manualSocFile
			fi

			# read manualMeterFile if file exists and manualMeterFile is newer than manualSocFile
			if [[ -f "$manualMeterFile" ]] && [ "$manualMeterFile" -nt "$manualSocFile" ]; then
				manualMeter=$(<$manualMeterFile)
			else
				# manualMeterFile does not exist or is outdated
				# update manualMeter with currentMeter
				manualMeter=$currentMeter
				echo $manualMeter > $manualMeterFile
			fi

			# read current soc
			if [[ -f "$socFile" ]]; then
				currentSoc=$(<$socFile)
			else
				currentSoc=$manualSoc
				echo $currentSoc > $socFile
			fi

			# calculate newSoc
			currentMeterDiff=$(echo "scale=3;$currentMeter - $manualMeter" | bc | sed 's/^\./0./')
			currentEffectiveMeterDiff=$(echo "scale=3;$currentMeterDiff * $efficiency / 100" | bc | sed 's/^\./0./')
			socDebugLog 1 "        Charged since last update: $currentMeterDiff kWh = $currentEffectiveMeterDiff kWh @ $efficiency% efficency"
			currentSocDiff=$(echo "scale=2;100 / $akkug * $currentEffectiveMeterDiff" | bc | sed 's/^\./0./')
			socDebugLog 1 "        Charged since last update: $currentEffectiveMeterDiff kWh of $akkug kWh = $currentSocDiff% SoC"
			newSoc=$(echo "scale=0;($manualSoc + $currentSocDiff) / 1" | bc)
			if (( newSoc > 100 )); then
				newSoc=100
			fi
			if (( newSoc < 0 )); then
				newSoc=0
			fi
			socDebugLog 1 "        Estimated SoC: $manualSoc% (last update) + $currentSocDiff% (extrapolation) = $newSoc% SoC"
			echo $newSoc > $socFile
		else
			# no current meter value for calculation -> Exit
			socDebugLog 1 "        ERROR: no meter value for calculation! ($meterFile)"
		fi
		socDebugLog 1 "    Manual Calculation ending"
	fi
else
	socDebugLog 1 "    SoC Update starting (Timer expired)"
	echo 0 > $soctimerfile
	echo 0 > $socsuccessfile
	
	sudo python3 $MODULEDIR/hyundaisoc.py $bluelink_email $bluelink_password $bluelink_pin $bluelink_vin $manualSocFile $CHARGEPOINT $socDebug $socsuccessfile >> $LOGFILE
	success=$(<$socsuccessfile)
	
	if ((success == 1)); then
		soc=$(<$manualSocFile)
		echo $soc > $socFile
		socDebugLog 1 "        SoC received: $soc%"
		
		if ((soccalc == 0)); then
			socDebugLog 1 "        Applying new SoC to openWB (no manual calculation)"

		fi
		if ((soccalc == 1)); then
			socDebugLog 1 "        Applying SoC and saving for manual calculation"
		fi
	else
		socDebugLog 1 "        SoC download not successful"
	fi
	
	touch $socFile
	socDebugLog 1 "    SoC Update ending"
fi

socDebugLog 1 "Bluelink SoC Module ending"
