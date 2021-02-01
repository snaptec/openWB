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
		manualSocFile="$RAMDISKDIR/manual_soc_lp2"
		manualMeterFile="$RAMDISKDIR/manual_soc_meter_lp2"
		socFile="$RAMDISKDIR/soc1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		peugeotSocFile="$RAMDISKDIR/peugeotsoc1"
		peugeotSocTime="$RAMDISKDIR/peugeotsoctime1"
		socIntervall=1 # update every 20 seconds if script is called every 10 seconds
		socOnlineIntervall=60 # update every 10 minutes if script is called every 10 seconds
		meterFile="$RAMDISKDIR/llkwhs1"
		ladungaktivFile="$RAMDISKDIR/ladungaktivlp2"
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		username=$mypeugeot_userlp2
		password=$mypeugeot_passlp2
		clientId=$mypeugeot_clientidlp2
		clientSecret=$mypeugeot_clientsecretlp2
		soccalc=$mypeugeot_soccalclp2
		chargestat=$(</var/www/html/openWB/ramdisk/chargestats1)
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		manualSocFile="$RAMDISKDIR/manual_soc_lp1"
		manualMeterFile="$RAMDISKDIR/manual_soc_meter_lp1"
		socFile="$RAMDISKDIR/soc"
		soctimerfile="$RAMDISKDIR/soctimer"
		peugeotSocFile="$RAMDISKDIR/peugeotsoc"
		peugeotSocTime="$RAMDISKDIR/peugeotsoctime"
		socIntervall=1 # update every 20 seconds if script is called every 10 seconds
		socOnlineIntervall=60 # update every 10 minutes if script is called every 10 seconds
		meterFile="$RAMDISKDIR/llkwh"
		ladungaktivFile="$RAMDISKDIR/ladungaktivlp1"
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		username=$mypeugeot_userlp1
		password=$mypeugeot_passlp1
		clientId=$mypeugeot_clientidlp1
		clientSecret=$mypeugeot_clientsecretlp1
		soccalc=$mypeugeot_soccalclp1
		chargestat=$(</var/www/html/openWB/ramdisk/chargestat)
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date --rfc-3339=seconds`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

incrementTimer(){
	soctimer=$((soctimer+1))
	echo $soctimer > $soctimerfile
}

soctimer=$(<$soctimerfile)

if (($soccalc == 0)); then #manual calculation not enabled, using existing logic
	timer=$(<$soctimerfile)
	if (( timer < $socOnlineIntervall )); then
		timer=$((timer+1))
		echo $timer > $soctimerfile
	else
		echo 0 > $soctimerfile
		sudo python $MODULEDIR/peugeotsoc.py $CHARGEPOINT $username $password $clientId $clientSecret
	fi
else	# manual calculation enabled, combining PSA module with manual calc method
	# if charging started this round fetch once from myPeugeot out of order
	if [[ $(<$ladungaktivFile) == 1 ]] && [ "$ladungaktivFile" -nt "$manualSocFile" ]; then
		socDebugLog "Status changed to loading. Fetching SoC from myPeugeot out of order."
		soctimer=0
		echo 0 > $soctimerfile
		sudo python $MODULEDIR/peugeotsoc.py $CHARGEPOINT $username $password $clientId $clientSecret
		echo $(<$peugeotSocFile) > $socFile
		echo $(<$peugeotSocFile) > $manualSocFile
		socDebugLog "Fetched from myPeugeot: $(<$peugeotSocFile)%"
	fi

	# if charging ist not active fetch SoC from myPeugeot
	if [[ $chargestat == "0" ]]; then
		if (( soctimer < $socOnlineIntervall )); then
			socDebugLog "Nothing to do yet. Incrementing timer. Extralong myPeugeot wait: $soctimer"
			incrementTimer
		else
			socDebugLog "Fetching SoC from myPeugeot"
			echo 0 > $soctimerfile
			sudo python $MODULEDIR/peugeotsoc.py $CHARGEPOINT $username $password $clientId $clientSecret
			dateofSoc=$(($(stat -c %Y "$socFile"))) # getting file mofified date in epoch
			diff=$(($dateofSoc - $(<$peugeotSocTime)))
			socDebugLog "Time of known SoC:   $(date -d @$dateofSoc +'%F %T')" # debug logging in readable time format
			socDebugLog "Time of fetched SoC: $(date -d @$(<$peugeotSocTime) +'%F %T')"
			socDebugLog "Fetched SoC time difference is $diff s"
			
			# if fetched SoC is newer than manualSoC
			if (( $diff < 0 )); then
				echo $(<$peugeotSocFile) > $socFile
				echo $(<$peugeotSocFile) > $manualSocFile
				socDebugLog "Fetched from myPeugeot: $(<$peugeotSocFile)% and using it."
			# if SoC is 0, so probably there ist no valid SoC known
			elif (( $(($(<$socFile))) == 0 )); then
				echo $(<$peugeotSocFile) > $socFile
				echo $(<$peugeotSocFile) > $manualSocFile
				socDebugLog "Fetched from myPeugeot: $(<$peugeotSocFile)% but nevertheless using it, because SoC was 0."
			else
				socDebugLog "Fetched from myPeugeot: $(<$peugeotSocFile)% but skipping it, because it is older than known SoC."
			fi
		fi
	# if charging is active calculate SoC manually
	else
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
				currentSocDiff=$(echo "100 / $akkug * $currentEffectiveMeterDiff" | bc | sed 's/\..*$//')
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
	fi
fi
