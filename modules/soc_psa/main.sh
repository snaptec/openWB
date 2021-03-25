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
		socIntervall=1 # update every 20 seconds if script is called every 10 seconds
		psaSocFile="$RAMDISKDIR/psasoc1"
		psaSocTime="$RAMDISKDIR/psasoctime1"
		meterFile="$RAMDISKDIR/llkwhs1"
		ladungaktivFile="$RAMDISKDIR/ladungaktivlp2"
		psaSocFile_last="$RAMDISKDIR/psasoclastlp2"
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		username=$psa_userlp2
		password=$psa_passlp2
		clientId=$psa_clientidlp2
		clientSecret=$psa_clientsecretlp2
		soccalc=$psa_soccalclp2
		manufacturer=$psa_manufacturerlp2
		socOnlineIntervall=$psa_intervallp2
		plugstat="$RAMDISKDIR/plugstats1"
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		manualSocFile="$RAMDISKDIR/manual_soc_lp1"
		manualMeterFile="$RAMDISKDIR/manual_soc_meter_lp1"
		socFile="$RAMDISKDIR/soc"
		soctimerfile="$RAMDISKDIR/soctimer"
		socIntervall=1 # update every 20 seconds if script is called every 10 seconds
		psaSocFile="$RAMDISKDIR/psasoc"
		psaSocTime="$RAMDISKDIR/psasoctime"
		meterFile="$RAMDISKDIR/llkwh"
		ladungaktivFile="$RAMDISKDIR/ladungaktivlp1"
		psaSocFile_last="$RAMDISKDIR/psasoclastlp1"
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		username=$psa_userlp1
		password=$psa_passlp1
		clientId=$psa_clientidlp1
		clientSecret=$psa_clientsecretlp1
		soccalc=$psa_soccalclp1
		manufacturer=$psa_manufacturerlp1
		socOnlineIntervall=$psa_intervallp1
		plugstat="$RAMDISKDIR/plugstat"
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

socLog(){
	timestamp=`date +"%Y-%m-%d %H:%M:%S"`	
	echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
}

incrementTimer(){
	soctimer=$((soctimer+1))
	echo $soctimer > $soctimerfile
}

ladungaktiv=$(<$ladungaktivFile)
soctimer=$(<$soctimerfile)
tmpintervall=$(( (socOnlineIntervall * 6) - 1 ))

if (($soccalc == 0)); then #manual calculation not enabled, using existing logic
	timer=$(<$soctimerfile)
	if (( timer < $tmpintervall )); then
		timer=$((timer+1))
		echo $timer > $soctimerfile
	else
		echo 0 > $soctimerfile
		sudo python $MODULEDIR/psasoc.py $CHARGEPOINT $username $password $clientId $clientSecret $manufacturer $soccalc
		if [[ $? != 0 ]]; then
			socLog "Fetching SoC from $manufacturer failed"
		fi
	fi
else	# manual calculation enabled, combining PSA module with manual calc method
	# if charging started this round fetch once from PSA out of order
	if [[ $ladungaktiv == 1 ]] && [ "$ladungaktivFile" -nt "$manualSocFile" ]; then
		socLog "Charging started. Fetching SoC from $manufacturer out of order."
		soctimer=0
		echo 0 > $soctimerfile
		sudo python $MODULEDIR/psasoc.py $CHARGEPOINT $username $password $clientId $clientSecret $manufacturer $soccalc
		if [[ $? == 0 ]]; then
			echo $(<$psaSocFile) > $socFile
			echo $(<$psaSocFile) > $manualSocFile
			echo $(<$psaSocFile) > $psaSocFile_last
			socLog "Fetched from $manufacturer: $(<$psaSocFile)% and using it."
		else
			echo $(<$socFile) > $manualSocFile	# verhindert dauerhaftes Abrufen, falls Onlineabfrage fehlschlägt
			socLog "Fetching SoC from $manufacturer failed. Setting $(<$socFile) as start SoC."
			
		fi
	# if charging is not active fetch SoC from PSA
	elif [[ $ladungaktiv == 0 ]]; then
		if (( soctimer < $tmpintervall )); then
			socDebugLog "Nothing to do yet. Incrementing timer. $socOnlineIntervall min online interval wait: $soctimer"
			incrementTimer
		else
			socLog "Fetching SoC from $manufacturer"
			echo 0 > $soctimerfile
			sudo python $MODULEDIR/psasoc.py $CHARGEPOINT $username $password $clientId $clientSecret $manufacturer $soccalc
			if [[ $? == 0 ]]; then
				# if fetched SoC is equal from last used fetched SoC and car is plugged in
				if [[ $(<$psaSocFile) == $(<$psaSocFile_last) ]] && [[ $(($(<$plugstat))) == 1 ]]; then
					socLog "Fetched from $manufacturer: $(<$psaSocFile)% but skipping as not different from last fetched SoC and car is plugged in."		
				# if SoC is 0, so probably there ist no valid SoC known
				elif (( $(($(<$socFile))) == 0 )); then
					echo $(<$psaSocFile) > $socFile
					echo $(<$psaSocFile) > $manualSocFile
					echo $(<$psaSocFile) > $psaSocFile_last
					socLog "Fetched from $manufacturer: $(<$psaSocFile)% and using it as previous SoC was 0."
				else
					dateofSoc=$(($(stat -c %Y "$socFile"))) # getting file modified date in epoch
					diff=$(($dateofSoc - $(<$psaSocTime)))
					socDebugLog "Time of known SoC:   $(date -d @$dateofSoc +'%F %T')" # debug logging in readable time format
					socDebugLog "Time of fetched SoC: $(date -d @$(<$psaSocTime) +'%F %T')"
					socDebugLog "Fetched SoC time difference is $diff s"	
					# if fetched SoC is newer than manualSoC
					if (( $diff < 90 )); then	# 90 wegen evtl. Uhrzeitabweichung zwischen Server und openWB
						echo $(<$psaSocFile) > $socFile
						echo $(<$psaSocFile) > $manualSocFile
						echo $(<$psaSocFile) > $psaSocFile_last
						socLog "Fetched from $manufacturer: $(<$psaSocFile)% and using it."
					else
						socLog "Fetched from $manufacturer: $(<$psaSocFile)% but skipping as not newer than current known SoC."
					fi
				fi
			else
				socLog "Fetching SoC from $manufacturer failed"
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
				currentSocDiff=$(echo "scale=5;100 / $akkug * $currentEffectiveMeterDiff" | bc | sed 's/\..*$//')
				socDebugLog "currentSocDiff: $currentSocDiff"
				newSoc=$(echo "$manualSoc + $currentSocDiff" | bc)
				if (( newSoc > 100 )); then
					socLog "newSoC above 100, setting to 100."
					newSoc=100
				fi
				if (( newSoc < 0 )); then
					socLog "newSoC below 100, setting to 0."
					newSoc=0
				fi
				socDebugLog "newSoc: $newSoc"
				echo $newSoc > $socFile
			else
				# no current meter value for calculation -> Exit
				socLog "ERROR: no meter value for calculation! ($meterFile)"
			fi
		fi
	fi
fi
