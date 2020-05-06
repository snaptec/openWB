#!/bin/bash

# Allow 3 minutes between RFID scan and plugin - else the CP gets disabled again
declare -r MaximumSecondsAfterRfidScanToAssignCp=180

# lastmanagement == 1 means that it's on openWB duo
if (( lastmanagement > 0 )); then
	declare -r InstalledChargePoints=2
else
	declare -r InstalledChargePoints=1
fi

declare -r StartScanDataLocation="web/logging/data/startRfidScanData"

#
# the main script that is called from outside world
rfid() {

	# prepare for normal debug output in level 2
	dbgWrite=:
	if (( debug == 2 )); then
		dbgWrite=echo
	fi

	NowItIs=$(date +%s)

	setLpPlugChangeState

	lasttag=$(<"ramdisk/readtag")

	if [[ $lasttag != "0" ]]; then
		if [ "$lasttag" == "$rfidlp1c1" ] || [ "$lasttag" == "$rfidlp1c2" ]  || [ "$lasttag" == "$rfidlp1c3" ] ; then
			echo "${lasttag},${NowItIs}" > ramdisk/rfidlp1
		fi
		if [ "$lasttag" == "$rfidlp2c1" ] || [ "$lasttag" == "$rfidlp2c2" ]  || [ "$lasttag" == "$rfidlp2c3" ] ; then
			echo "${lasttag},${NowItIs}" > ramdisk/rfidlp2
		fi
		if [ "$lasttag" == "$rfidstop" ] || [ "$lasttag" == "$rfidstop2" ] || [ "$lasttag" == "$rfidstop3" ] ; then
			echo 3 > ramdisk/lademodus
		fi

		if [ "$lasttag" == "$rfidsofort" ] || [ "$lasttag" == "$rfidsofort2" ] || [ "$lasttag" == "$rfidsofort3" ]  ; then
			echo 0 > ramdisk/lademodus
		fi

		if [ "$lasttag" == "$rfidminpv" ] || [ "$lasttag" == "$rfidminpv2" ] || [ "$lasttag" == "$rfidminpv3" ]  ; then
			echo 1 > ramdisk/lademodus
		fi

		if [ "$lasttag" == "$rfidnurpv" ] || [ "$lasttag" == "$rfidnurpv2" ] || [ "$lasttag" == "$rfidnurpv3" ]   ; then
			echo 2 > ramdisk/lademodus
		fi

		if [ "$lasttag" == "$rfidstandby" ] || [ "$lasttag" == "$rfidstandby2" ] || [ "$lasttag" == "$rfidstandby3" ] ; then
			echo 4 > ramdisk/lademodus
		fi
		if [ "$lasttag" == "$rfidlp1start1" ] || [ "$lasttag" == "$rfidlp1start2" ] || [ "$lasttag" == "$rfidlp1start3" ] ; then
			mosquitto_pub -r -t openWB/set/lp/1/ChargePointEnabled -m "1"
			lp1enabled=1
		fi
		if [ "$lasttag" == "$rfidlp2start1" ] || [ "$lasttag" == "$rfidlp2start2" ] || [ "$lasttag" == "$rfidlp2start3" ] ; then
			mosquitto_pub -r -t openWB/set/lp/2/ChargePointEnabled -m "1"
			lp2enabled=1
		fi

		# check all CPs that we support for whether the tag is valid for that CP
		for ((currentCp=1; currentCp<=InstalledChargePoints; currentCp++)); do
			checkTagValidAndSetStartScanData $currentCp
		done

		echo "${lasttag},${NowItIs}" > "ramdisk/rfidlasttag"
		echo 0 > "ramdisk/readtag"
	fi

	#
	# handle special behaviour for slave mode
	#
	if (( slavemode == 1 )); then

		# handle plugin only if we have valid un-assigned start data (i.e. an RFID-scan that has not yet been assigned to a CP)
		if [ -f "${StartScanDataLocation}" ]; then

			# extract fragments of start data
			startData=$(<"${StartScanDataLocation}")
			IFS=',' read -r -a startDataSegments <<< "$startData"

			if (( pluggedLp > 0 )) || ( (( InstalledChargePoints == 1 )) && (( plugstat == 1 )) && [[ ! -f "${StartScanDataLocation}Lp1" ]] ); then

				local pluggedLpToUse=$pluggedLp
				if (( pluggedLp == 0)); then
					# happens for openWB single if already plugged in
					pluggedLp=1
				fi

				startDataForPluggedLp="${startData}"
				echo "$NowItIs: Charge point #${pluggedLp} has been plugged in - recording accounting start data"
				echo "${startDataForPluggedLp}" > "${StartScanDataLocation}Lp${pluggedLp}"
				rm -f "${StartScanDataLocation}"
			else
				secondsSinceRfidScan=$(( NowItIs - startDataSegments[0] ))

				$dbgWrite "$NowItIs: Not yet plugged in any CP ${secondsSinceRfidScan} seconds after RFID scan. Further waiting for plugin for at most ${MaximumSecondsAfterRfidScanToAssignCp} seconds"

				# check for timeout of start data
				if (( secondsSinceRfidScan > MaximumSecondsAfterRfidScanToAssignCp )); then
					echo "$NowItIs: Timeout (${secondsSinceRfidScan} > ${MaximumSecondsAfterRfidScanToAssignCp} seconds) waiting for plugin after RFID scan. Disabling the CP and deleting accounting data."

					# in case of timeout we disable all CPs that are NOT plugged in right now
					for ((currentCp=1; currentCp<=InstalledChargePoints; currentCp++)); do
						if [[ "${lpsPlugStat[$currentCp]}" -ne "1" ]]; then
							echo "$NowItIs: Disabling CP #${currentCp} as it's still unplugged after timeout of RFID tag scan has been exceeded"
							mosquitto_pub -r -q 2 -t "openWB/set/lp${currentCp}/ChargePointEnabled" -m "0"
							eval lp${currentCp}enabled=0
						fi
					done

					rm -f "${StartScanDataLocation}"
				fi
			fi
		fi

		# handle un-plug
		for ((currentCp=1; currentCp<=InstalledChargePoints; currentCp++)); do
			if (( unpluggedLps[$currentCp] > 0 )); then
				echo "$NowItIs: Charge point #${currentCp} has been UNplugged - if running, stop sending accounting data (after one final transmission)"

				# one final transmission of accounting data ...
				sendAccounting $currentCp

				# ... before we disabled it by removing the start info
				rm -f "${StartScanDataLocation}Lp${currentCp}"
			fi

			# finally actually transmit the accounting data
			sendAccounting $currentCp
		done
	fi
}


# sends the accounting data via MQTT if start data for given charge point is available
sendAccounting() {

	chargePoint=$1

	if [ -f "${StartScanDataLocation}Lp${chargePoint}" ]; then

		if (( lpsPlugStat[$chargePoint] == 255 )); then
			echo "$NowItIs: Plug state for CP ${chargePoint} contains garbage. Not sending accounting data"
			return
		fi

		getCpChargestat $chargePoint
		local chargestatToUse=$?
		if (( chargestatToUse == 255 )); then
			echo "$NowItIs: Charge state for CP ${chargePoint} contains garbage. Not sending accounting data"
			return
		fi

		$dbgWrite "$NowItIs: Sending accounting data for CP #${chargePoint}"
		startDataAcc=$(<"${StartScanDataLocation}Lp${chargePoint}")
		mosquitto_pub -r -q 2 -t "openWB/lp/${chargePoint}/Accounting" -m "${startDataAcc},$NowItIs,${lpsPlugStat[$chargePoint]},$chargestatToUse,$llkwh"
	fi
}


# determine if any of LP1 or LP2 has just been plugged in
# if it has, pluggedLp will be set to the CP number (1 or 2).
# if it has NOT, pluggedLp will be set to 0
setLpPlugChangeState() {

	if [ ! -f "ramdisk/accPlugstatChangeDetectLp1" ]; then
		echo "$plugstat" > "ramdisk/accPlugstatChangeDetectLp1"
	fi
	local oplugstat=$(<"ramdisk/accPlugstatChangeDetectLp1")

	if [ ! -f "ramdisk/accPlugstatChangeDetectLp2" ]; then
		echo "$plugstats1" > "ramdisk/accPlugstatChangeDetectLp2"
	fi
	local oplugstats1=$(<"ramdisk/accPlugstatChangeDetectLp2")

	pluggedLp=0

	getCpPlugstat 1
	local plugstatToUse1=$?
	getCpPlugstat 2
	local plugstatToUse2=$?

	lpsPlugStat=(0 $plugstatToUse1 $plugstatToUse2)
	unpluggedLps=(0 0 0)
	pluggedLps=(0 0 0)

	# first check LP2 as the last one will win for plugin and it seems more logical to let LP1 win
	if [ -n "$plugstats1" ]; then
		if (( lpsPlugStat[2] == oplugstats1 )); then
			:
		elif (( lpsPlugStat[2] == 1 )) && (( oplugstats1 == 0 )); then
			echo "$NowItIs: LP 2 plugged in"
			pluggedLp=2
			pluggedLps[2]=1
		elif (( lpsPlugStat[2] == 0 )) && (( oplugstats1 == 1 )); then
			echo "$NowItIs: LP 2 un-plugged"
			unpluggedLps[2]=1
		else
			echo "$NowItIs: LP 2 unkown plug state '${plugstats1}'"
		fi

		echo ${lpsPlugStat[2]} > "ramdisk/accPlugstatChangeDetectLp2"
	fi

	# finally check LP1 so it wins
	if [ -n "$plugstat" ]; then
		if (( lpsPlugStat[1] == oplugstat )); then
			:
		elif (( lpsPlugStat[1] == 1 )) && (( oplugstat == 0 )); then
			echo "$NowItIs: LP 1 plugged in"
			pluggedLp=1
			pluggedLps[1]=1
		elif (( lpsPlugStat[1] == 0 )) && (( oplugstat == 1 )); then
			echo "$NowItIs: LP 1 un-plugged"
			unpluggedLps[1]=1
		else
			echo "$NowItIs: LP 1 unkown plug state '${plugstat}'"
		fi

		echo ${lpsPlugStat[1]} > "ramdisk/accPlugstatChangeDetectLp1"
	fi
}


# checks if the tag stored in $lasttag is valid for the charge point passed in $1
checkTagValidAndSetStartScanData() {

	local chargePoint=$1

	# if we're in slave mode on an openWB dual and the LP has not just been plugged in (in same control interval as the RFID scan)
	# we completely ignore the scan as we cannot associate it with a plugin operation
	if (( slavemode == 1 )) && (( lpsPlugStat[$chargePoint] > 0 )) && (( pluggedLps[$chargePoint] != 1 )) && ( (( lastmanagement != 0 )) || (( chargePoint > 1 )) ); then
		echo "$NowItIs: Ignoring RFID scan of tag '${lasttag}' for CP #${chargePoint} because that CP is not in 'unplugged' state (plugstatToUse == ${lpsPlugStat[$chargePoint]}, justPlugged == ${pluggedLps[$chargePoint]}, lastmanagement=${lastmanagement})"
		return 0
	fi

	local ramdiskFileForCp="ramdisk/AllowedRfidsForLp${chargePoint}"
	if [ ! -f "$ramdiskFileForCp" ]; then
		return 1
	fi

	local rfidlist=$(<"$ramdiskFileForCp")
	$dbgWrite "$NowItIs: rfidlist(LP${chargePoint})='${rfidlist}'"

	# leave right away if we have no list of valid RFID tags for the charge point
	if [ -z "$rfidlist" ]; then
		echo "$NowItIs: Empty 'allowed tags list' for CP #${chargePoint} after scan of tag '${lasttag}'"
		return 1
	fi

	for i in $(echo $rfidlist | sed "s/,/ /g")
	do
		if [ "$lasttag" == "$i" ] ; then

			# found valid RFID tag for the charge point
			# write at-scan accounting info
			echo "$NowItIs,$lasttag,$llkwh" > "${StartScanDataLocation}"

			# and the ramdisk file for legacy ladelog
			echo $lasttag > "ramdisk/rfidlp${chargePoint}"

			mosquitto_pub -r -q 2 -t "openWB/set/lp${chargePoint}/ChargePointEnabled" -m "1"
			eval lp${chargePoint}enabled=1
			echo "$NowItIs: Start waiting for ${MaximumSecondsAfterRfidScanToAssignCp} seconds for CP #${chargePoint} to get plugged in after RFID scan of '$lasttag' @ meter value $llkwh (justPlugged == ${pluggedLps[$chargePoint]})"

			return 0
		fi
	done

	echo "$NowItIs: RFID tag '${lasttag}' is not authorized to enable this CP"

	return 1
}

# returns the plugstat value for the given CP as exit code
getCpPlugstat() {

	local chargePoint=$1
	local returnstat=255

	if (( $chargePoint == 1 )); then
		returnstat=$plugstat
	elif (( $chargePoint == 2 )); then
		returnstat=$plugstats1
	else
		echo "$NowItIs: Don't know how to get plugged status of CP #${chargePoint}. Returning 255"
		returnstat=255
	fi

	# heal cases where $plugstat contains garbage
	if [ -z "${returnstat}" ]; then
		returnstat=255
	fi

	return $returnstat
}


# returns the chargestat value for the given CP as exit code
getCpChargestat() {

	local chargePoint=$1
	local returnstat=255

	if (( $chargePoint == 1 )); then
		returnstat=$chargestat
	elif (( $chargePoint == 2 )); then
		returnstat=$chargestats1
	else
		echo "$NowItIs: Don't know how to get chage status of CP #${chargePoint}. Returning 255"
		returnstat=255
	fi

	# heal cases where $chargestat contains garbage
	if [ -z "${returnstat}" ]; then
		returnstat=255
	fi

	return $returnstat
}