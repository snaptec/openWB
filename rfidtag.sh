#!/bin/bash

# Allow 3 minutes between RFID scan and plugin - else the CP gets disabled again
MaximumSecondsAfterRfidScanToAssignCp=180
NumberOfSupportedChargePoints=2


#
# the main script that is called from outside world
rfid() {

	# prepare for normal debug output in level 2
	dbgWrite=:
	if (( debug == 2 )); then
		dbgWrite=echo
	fi

	NowItIs=$(date +%s)

	lasttag=$(<"ramdisk/readtag")

	if [[ $lasttag != "0" ]]; then
		if [ $lasttag == $rfidlp1c1 ] || [ $lasttag == $rfidlp1c2 ]  || [ $lasttag == $rfidlp1c3 ] ; then
			echo $lasttag > ramdisk/rfidlp1
		fi
		if [ $lasttag == $rfidlp2c1 ] || [ $lasttag == $rfidlp2c2 ]  || [ $lasttag == $rfidlp2c3 ] ; then
			echo $lasttag > ramdisk/rfidlp2
		fi
		if [ $lasttag == $rfidstop ] || [ $lasttag == $rfidstop2 ] || [ $lasttag == $rfidstop3 ] ; then
			echo 3 > ramdisk/lademodus
		fi

		if [ $lasttag == $rfidsofort ] || [ $lasttag == $rfidsofort2 ] || [ $lasttag == $rfidsofort3 ]  ; then
			echo 0 > ramdisk/lademodus
		fi

		if [ $lasttag == $rfidminpv ] || [ $lasttag == $rfidminpv2 ] || [ $lasttag == $rfidminpv3 ]  ; then
			echo 1 > ramdisk/lademodus
		fi

		if [ $lasttag == $rfidnurpv ] || [ $lasttag == $rfidnurpv2 ] || [ $lasttag == $rfidnurpv3 ]   ; then
			echo 2 > ramdisk/lademodus
		fi

		if [ $lasttag == $rfidstandby ] || [ $lasttag == $rfidstandby2 ] || [ $lasttag == $rfidstandby3 ] ; then
			echo 4 > ramdisk/lademodus
		fi
		if [ $lasttag == $rfidlp1start1 ] || [ $lasttag == $rfidlp1start2 ] || [ $lasttag == $rfidlp1start3 ] ; then
			mosquitto_pub -r -t openWB/set/lp1/ChargePointEnabled -m "1"
		fi
		if [ $lasttag == $rfidlp2start1 ] || [ $lasttag == $rfidlp2start2 ] || [ $lasttag == $rfidlp2start3 ] ; then
			mosquitto_pub -r -t openWB/set/lp2/ChargePointEnabled -m "1"
		fi

		# check all CPs that we support for whether the tag is valid for that CP
		for ((currentCp=1; currentCp<=NumberOfSupportedChargePoints; currentCp++)); do
			checkTagValidAndSetStartScanData $currentCp
		done

		echo $lasttag > "ramdisk/rfidlasttag"
		echo 0 > "ramdisk/readtag"
	fi


	#
	# handle special behaviour for slave mode
	#
	if (( slavemode == 1 )); then

		setLpPlugChangeState

		# handle plugin only if we have valid un-assigned start data (i.e. an RFID-scan that has not yet been assigned to a CP)
		if [ -f "ramdisk/startRfidScanData" ]; then

			# extract fragments of start data
			startData=$(<"ramdisk/startRfidScanData")
			IFS=',' read -r -a startDataSegments <<< "$startData"

			if (( pluggedLp > 0 )); then

				startDataForPluggedLp="${startData}"
				echo "$NowItIs: Charge point #${pluggedLp} has been plugged in - recording accounting start data"
				echo "${startDataForPluggedLp}" > "ramdisk/startRfidScanDataLp${pluggedLp}"
				rm -f "ramdisk/startRfidScanData"
			else
				secondsSinceRfidScan=$(( NowItIs - startDataSegments[0] ))

				$dbgWrite "$NowItIs: Not yet plugged in any CP ${secondsSinceRfidScan} seconds after RFID scan. Further waiting for plugin for at most ${MaximumSecondsAfterRfidScanToAssignCp} seconds"

				# check for timeout of start data
				if (( secondsSinceRfidScan > MaximumSecondsAfterRfidScanToAssignCp )); then
					echo "$NowItIs: Timeout (${secondsSinceRfidScan} > ${MaximumSecondsAfterRfidScanToAssignCp} seconds) waiting for plugin after RFID scan. Disabling the CP and deleting accounting data."

					# in case of timeout we disable all CPs that are NOT plugged in right now
					for ((currentCp=1; currentCp<=NumberOfSupportedChargePoints; currentCp++)); do
						if [[ "${lpsPlugStat[$currentCp]}" -eq "0" ]]; then
							echo "$NowItIs: Disabling CP #${currentCp} as it's still unplugged after timeout of RFID tag scan has been exceeded"
							mosquitto_pub -r -q 2 -t "openWB/set/lp${currentCp}/ChargePointEnabled" -m "0"
						fi
					done

					rm -f "ramdisk/startRfidScanData"
				fi
			fi
		fi

		# handle un-plug
		for ((currentCp=1; currentCp<=NumberOfSupportedChargePoints; currentCp++)); do
			if (( unpluggedLps[$currentCp] > 0 )); then
				echo "$NowItIs: Charge point #${currentCp} has been UNplugged - stop sending accounting data after one final transmission"

				# one final transmission of accounting data ...
				sendAccounting $currentCp

				# ... before we disabled it by removing the start info
				rm -f "ramdisk/startRfidScanDataLp${currentCp}"
			fi

			# finally actually transmit the accounting data
			sendAccounting $currentCp
		done
	fi
}


# sends the accounting data via MQTT if start data for given charge point is available
sendAccounting() {

	chargePoint=$1

	if [ -f "ramdisk/startRfidScanDataLp${chargePoint}" ]; then
		$dbgWrite "$NowItIs: Sending accounting data for CP #${chargePoint}"
		startDataAcc=$(<"ramdisk/startRfidScanDataLp${chargePoint}")
		mosquitto_pub -r -q 2 -t "openWB/lp/${chargePoint}/Accounting" -m "${startDataAcc},$NowItIs,$plugstat,$chargestat,$llkwh"
	fi
}


# determine if any of LP1 or LP2 has just been plugged in
# if it has, pluggedLp will be set to the CP number (1 or 2).
# if it has NOT, pluggedLp will be set to 0
setLpPlugChangeState() {

	oplugstat=$(<"ramdisk/accPlugstatChangeDetectLp1")
	oplugstats1=$(<"ramdisk/accPlugstatChangeDetectLp2")

	if [ -f "ramdisk/mockedPlugstat" ]; then
		plugstat=$(<"ramdisk/mockedPlugstat")
	fi

	if [ -f "ramdisk/mockedPlugstats1" ]; then
		plugstats1=$(<"ramdisk/mockedPlugstats1")
	fi

	pluggedLp=0
	lpsPlugStat=($plugstat $plugstats1)
	unpluggedLps=(0 0 0)

	# first check LP2 as the last one will win for plugin and it seems more logical to let LP1 win
	if (( plugstats1 == 1 )) && (( oplugstats1 == 0 )); then
		echo "$NowItIs: LP 2 plugged in"
		pluggedLp=2
	elif (( plugstats1 == 0 )) && (( oplugstats1 == 1 )); then
		echo "$NowItIs: LP 2 un-plugged"
		unpluggedLps[2]=1
	fi

	echo $plugstats1 > "ramdisk/accPlugstatChangeDetectLp2"

	# finally check LP1 so it wins
	if (( plugstat == 1 )) && (( oplugstat == 0 )); then
		echo "$NowItIs: LP 1 plugged in"
		pluggedLp=1
	elif (( plugstat == 0 )) && (( oplugstat == 1 )); then
		echo "$NowItIs: LP 1 un-plugged"
		unpluggedLps[1]=1
	fi

	echo $plugstat > "ramdisk/accPlugstatChangeDetectLp1"
}


# checks if the tag stored in $lasttag is valid for the charge point passed in $1
checkTagValidAndSetStartScanData() {

	chargePoint=$1

	ramdiskFileForCp="ramdisk/AllowedRfidsForLp${chargePoint}"
	if [ ! -f "$ramdiskFileForCp" ]; then
		return 1
	fi

	rfidlist=$(<"$ramdiskFileForCp")
	$dbgWrite "$NowItIs: rfidlist(LP${chargePoint})='${rfidlist}'"

	# leave right away if we have no list of valid RFID tags for the charge point
	if [ -z "$rfidlist" ]; then
		echo "$NowItIs: Empty 'allowed tags list' for CP #${chargePoint} after scan of tag '${lasttag}'"
		return 1
	fi

	for i in $(echo $rfidlist | sed "s/,/ /g")
	do
		if [ $lasttag == $i ] ; then

			# found valid RFID tag for the charge point
			echo "$NowItIs,$lasttag,$llkwh" > "ramdisk/startRfidScanData"
			mosquitto_pub -r -q 2 -t "openWB/set/lp${chargePoint}/ChargePointEnabled" -m "1"
			echo "$NowItIs: Start waiting for LP${chargePoint} plugin after RFID scan of '$lasttag' @ meter value $llkwh"

			return 0
		fi
	done

	echo "$NowItIs: RFID tag '${lasttag}' is not authorized to enable this CP"

	return 1
}
