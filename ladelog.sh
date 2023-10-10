#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

# get name of current logfile
monthlyfile="${OPENWBBASEDIR}/web/logging/data/ladelog/$(date +%Y%m).csv"
if [ ! -f "$monthlyfile" ]; then
	echo "$monthlyfile"
fi
openwbDebugLog "CHARGESTAT" 1 "### start (->$monthlyfile)"

# check for special charge modes
nachtladenstate=$(<"${RAMDISKDIR}/nachtladenstate")       # "Nachtladen" LP1
nachtladen2state=$(<"${RAMDISKDIR}/nachtladen2state")     # "Morgensladen" LP1
nachtladenstates1=$(<"${RAMDISKDIR}/nachtladenstates1")   # "Nachtladen" LP2
nachtladen2states1=$(<"${RAMDISKDIR}/nachtladen2states1") # "Morgensladen" LP2
if ((nachtladenstate == 0)) && ((nachtladen2state == 0)) && ((nachtladenstates1 == 0)) && ((nachtladen2states1 == 0)); then
	lmodus=$(<"${RAMDISKDIR}/lademodus")
else
	# "Nachtladen" or "Morgensladen" is configured, set charge mode to "7"
	lmodus=7
	openwbDebugLog "CHARGESTAT" 2 "\"Nachtladen\" or \"Morgensladen\" active. \"lmodus=7\""
fi
if [ -e "${RAMDISKDIR}/loglademodus" ]; then
	lademodus=$(<"${RAMDISKDIR}/loglademodus")
	loglademodus=$lademodus
	openwbDebugLog "CHARGESTAT" 2 "\"loglademodus\"=$loglademodus"
fi

getTimeDiffString() {
	minutes=$1

	if ((minutes >= 60)); then
		text="$((minutes / 60)) H $((minutes % 60)) Min"
	elif ((minutes >= 0)); then
		text="$minutes Min"
	else
		text="--"
	fi
	echo "$text"
}

# function for charge points 1 to 8
processChargepoint() {
	chargePointNumber=$1
	# quirk to handle ugly file naming
	case $chargePointNumber in
	1)
		soc=$(<"${RAMDISKDIR}/soc")
		chargePointKey="lp1"
		chargePointKey2=""
		chargePointKey3=$chargePointKey2
		chargePointActivated=1 # charge point 1 is always activated
		;;
	2)
		soc=$(<"${RAMDISKDIR}/soc1")
		chargePointKey="lp2"
		chargePointKey2="s1"
		chargePointKey3=$chargePointKey2
		chargePointActivated=$lastmanagement
		;;
	3)
		soc=0
		chargePointKey="lp3"
		chargePointKey2="s2"
		chargePointKey3=$chargePointKey
		chargePointActivated=$lastmanagements2
		;;
	*)
		soc=0
		chargePointKey="lp$1"
		chargePointKey2=$chargePointKey
		chargePointKey3=$chargePointKey
		chargePointActivatedVariableName="lastmanagement$chargePointKey"
		chargePointActivated=${!chargePointActivatedVariableName}
		;;
	esac

	chargePointNameVariableName="${chargePointKey}name"
	if ((chargePointActivated == 1)); then
		openwbDebugLog "CHARGESTAT" 1 "# processing charge point $chargePointNumber (${!chargePointNameVariableName})"
		# get soc
		if ((soc > 0)); then
			openwbDebugLog "CHARGESTAT" 1 "soc detected: $soc%"
			soctext=", bei $soc %SoC."
		else
			openwbDebugLog "CHARGESTAT" 2 "soc not configured or zero"
			soctext="."
		fi
		# get rfid tag
		rfid=$(<"${RAMDISKDIR}/rfid${chargePointKey}")
		rfid=$(cut -d ',' -f 1 <<<"$rfid")
		# get actual charge power
		ladeleistung=$(<"${RAMDISKDIR}/llaktuell${chargePointKey2}")
		# get actual meter value
		llkwh=$(<"${RAMDISKDIR}/llkwh${chargePointKey2}")
		openwbDebugLog "CHARGESTAT" 1 "rfid=$rfid; power=$ladeleistung; meter=$llkwh"
		# get plug state
		plugstat=$(<"${RAMDISKDIR}/plugstat${chargePointKey3}")
		if ((plugstat == 1)); then
			# a car is connected
			openwbDebugLog "CHARGESTAT" 1 "car connected: plugstat=$plugstat"
			pluggedladungakt=$(<"${RAMDISKDIR}/pluggedladungakt${chargePointKey}")
			if ((pluggedladungakt == 0)); then
				# new charge detected
				openwbDebugLog "CHARGESTAT" 1 "new charge detected; meter=$llkwh"
				# write actual meter value as start value since plugged in
				echo "$llkwh" >"${RAMDISKDIR}/pluggedladung${chargePointKey}startkwh"
				# note ourself about tracking this charge
				echo 1 >"${RAMDISKDIR}/pluggedladungakt${chargePointKey}"
			fi
			if (("stopchargeafterdisc$chargePointKey" == 1)); then
				openwbDebugLog "CHARGESTAT" 2 "\"stopchargeafterdisc\" set, charge point will be locked after unplug is detected"
				boolstopchargeafterdisc=$(<"${RAMDISKDIR}/boolstopchargeafterdisc${chargePointKey}")
				if ((boolstopchargeafterdisc == 0)); then
					# note ourself to lock this charge point after disconnect
					echo 1 >"${RAMDISKDIR}/boolstopchargeafterdisc${chargePointKey}"
				fi
			fi
			# read start meter value since plugged
			pluggedladungstartkwh=$(<"${RAMDISKDIR}/pluggedladung${chargePointKey}startkwh")
			# calculate actual meter value difference since plugged
			pluggedladungbishergeladen=$(echo "scale=2;($llkwh - $pluggedladungstartkwh)/1" | bc | sed 's/^\./0./')
			echo "$pluggedladungbishergeladen" >"${RAMDISKDIR}/pluggedladungbishergeladen${chargePointKey}"
			openwbDebugLog "CHARGESTAT" 1 "charged since plugged: $llkwh - $pluggedladungstartkwh = $pluggedladungbishergeladen"
			# reset unplug timer
			echo 0 >"${RAMDISKDIR}/pluggedtimer${chargePointKey}"
		else
			# no car connected
			openwbDebugLog "CHARGESTAT" 1 "car not connected: plugstat=$plugstat"
			pluggedtimer=$(<"${RAMDISKDIR}/pluggedtimer${chargePointKey}")
			if ((pluggedtimer < 5)); then
				# increment unplug timer
				pluggedtimer=$((pluggedtimer + 1))
				echo "$pluggedtimer" >"${RAMDISKDIR}/pluggedtimer${chargePointKey}"
				openwbDebugLog "CHARGESTAT" 2 "pluggedtimer=$pluggedtimer"
			else
				# unplug timer reached 60s (in normal control loop speed)
				# stop actual tracked charge
				echo 0 >"${RAMDISKDIR}/pluggedladungakt${chargePointKey}"
				openwbDebugLog "CHARGESTAT" 2 "unplug detected"
				# lock this charge point if configured
				if (("stopchargeafterdisc$chargePointKey" == 1)); then
					openwbDebugLog "CHARGESTAT" 2 "locking charge point"
					boolstopchargeafterdisc=$(<"${RAMDISKDIR}/boolstopchargeafterdisc${chargePointKey}")
					if ((boolstopchargeafterdisc == 1)); then
						echo 0 >"${RAMDISKDIR}/boolstopchargeafterdisc${chargePointKey}"
						mosquitto_pub -r -t "openWB/set/lp/${chargePointNumber}/ChargePointEnabled" -m "0"
					fi
				fi
			fi
		fi
		if ((ladeleistung > 100)); then
			# charge point is charging
			openwbDebugLog "CHARGESTAT" 1 "car is charging"
			if [ -e "${RAMDISKDIR}/ladeustart${chargePointKey2}" ]; then
				# charge already running
				openwbDebugLog "CHARGESTAT" 2 "this charge was already detected"
				# calculate actual energy charged
				ladelstart=$(<"${RAMDISKDIR}/ladelstart${chargePointKey2}")
				bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" | bc | sed 's/^\./0./')
				echo "$bishergeladen" >"${RAMDISKDIR}/aktgeladen${chargePointKey2}"
				# calculate range charged
				averageConsumptionVariableName="durchs$chargePointKey"
				gelr=$(echo "scale=0;$bishergeladen * 100 / ${!averageConsumptionVariableName}" | bc)
				echo "$gelr" >"${RAMDISKDIR}/gelr${chargePointKey}"
				# calculate time remaining if energy limit is set
				energyChargeLimitVariableName="lademkwh$chargePointKey2"
				restzeit=$(echo "scale=0;(${!energyChargeLimitVariableName} - $bishergeladen) * 1000 * 60 / $ladeleistung" | bc)
				echo "$restzeit" >"${RAMDISKDIR}/restzeit${chargePointKey}m"
				# format time charged
				restzeittext=$(getTimeDiffString "$restzeit")
				echo "$restzeittext" >"${RAMDISKDIR}/restzeit${chargePointKey}"
				openwbDebugLog "CHARGESTAT" 1 "energyCharged: ${llkwh} - ${ladelstart}=${bishergeladen}kWh; rangeCharged=${gelr}km; timeRemaining=${restzeit}m ($restzeittext)"
			else
				# new charge detected
				openwbDebugLog "CHARGESTAT" 1 "new charge detected"
				echo 1 >"${RAMDISKDIR}/ladungaktiv${chargePointKey}"
				# save actual timestamp for this charge
				touch "${RAMDISKDIR}/ladeustart${chargePointKey2}"
				echo -e "$(date +%d.%m.%y-%H:%M)" >"${RAMDISKDIR}/ladeustart${chargePointKey2}"
				echo -e "$(date +%s)" >"${RAMDISKDIR}/ladeustarts${chargePointKey2}"
				# save actual charge mode for this charge
				echo "$lmodus" >"${RAMDISKDIR}/loglademodus"
				# save actual meter value es start for this charge
				echo "$llkwh" >"${RAMDISKDIR}/ladelstart${chargePointKey2}"
				# send push message if configured
				if ((pushbenachrichtigung == 1)); then
					if ((pushbstartl == 1)); then
						openwbDebugLog "CHARGESTAT" 2 "sending push notification for charge point \"${!chargePointNameVariableName}\""
						"${OPENWBBASEDIR}/runs/pushover.sh" "${!chargePointNameVariableName} Ladung gestartet$soctext"
					fi
				fi
				openwbDebugLog "CHARGESTAT" 0 "LP${chargePointNumber}, Ladung gestartet"
			fi
			# reset our charge stop timer
			echo 0 >"${RAMDISKDIR}/llog${chargePointKey2}"
		else
			# charge point is not charging
			openwbDebugLog "CHARGESTAT" 1 "car is not charging"
			llog=$(<"${RAMDISKDIR}/llog${chargePointKey2}")
			if ((llog < 5)); then
				# increment charge stop timer
				llog=$((llog + 1))
				echo "$llog" >"${RAMDISKDIR}/llog${chargePointKey2}"
				openwbDebugLog "CHARGESTAT" 2 "llog=$llog"
			else
				# charge stop timer reached 60s (in normal control loop speed)
				if [ -e "${RAMDISKDIR}/ladeustart${chargePointKey2}" ]; then
					# a charge just finished
					openwbDebugLog "CHARGESTAT" 1 "end of charge detected"
					# reset detected charge
					echo 0 >"${RAMDISKDIR}/ladungaktiv${chargePointKey}"
					# clear time remaining
					echo "--" >"${RAMDISKDIR}/restzeit${chargePointKey}"
					# calculate energy charged
					ladelstart=$(<"${RAMDISKDIR}/ladelstart${chargePointKey2}")
					bishergeladen=$(echo "scale=2;($llkwh - $ladelstart)/1" | bc | sed 's/^\./0./')
					# calculate range charged
					averageConsumptionVariableName="durchs$chargePointKey"
					gelr=$(echo "scale=0;$bishergeladen * 100 / ${!averageConsumptionVariableName}" | bc)
					# calculate time charged
					start=$(<"${RAMDISKDIR}/ladeustart${chargePointKey2}")
					ladeustarts=$(<"${RAMDISKDIR}/ladeustarts${chargePointKey2}")
					jetzt=$(date +%d.%m.%y-%H:%M)
					jetzts=$(date +%s)
					ladedauer=$(((jetzts - ladeustarts) / 60))
					ladedauers=$((jetzts - ladeustarts))
					# calculate average power
					ladegeschw=$(echo "scale=2;$bishergeladen * 60 * 60 / $ladedauers" | bc)
					# format time charged
					ladedauertext=$(getTimeDiffString "$ladedauer")
					# add charge log entry
					if ((chargePointNumber < 3)); then
						lademoduslogvalue=$loglademodus
					else
						lademoduslogvalue=$lademodus
					fi
					# calculate costs
					kosten=$(echo "scale=2;$bishergeladen * $preisjekwh" | bc)
					# save final values
					sed -i "1i$start,$jetzt,$gelr,$bishergeladen,$ladegeschw,$ladedauertext,$chargePointNumber,$lademoduslogvalue,$rfid,$kosten" "$monthlyfile"
					# send push message if configured
					if ((pushbenachrichtigung == 1)); then
						if ((pushbstopl == 1)); then
							openwbDebugLog "CHARGESTAT" 2 "sending push notification for charge point \"${!chargePointNameVariableName}\""
							"${OPENWBBASEDIR}/runs/pushover.sh" "${!chargePointNameVariableName} Ladung gestoppt. $bishergeladen kWh in $ladedauertext mit durchschnittlich $ladegeschw kW geladen$soctext"
						fi
					fi
					# clear detected charge start
					rm "${RAMDISKDIR}/ladeustart${chargePointKey2}"
					openwbDebugLog "CHARGESTAT" 0 "LP$chargePointNumber, Ladung gestoppt"
					openwbDebugLog "CHARGESTAT" 1 "Ladelogeintrag: start=$start; end=$jetzt; timeCharged=${ladedauer}m ($ladedauertext); energyCharged=${bishergeladen}kWh; rangeCharged=${gelr}km; averagePower=${ladegeschw}kW; costs=${kosten}"
				fi
			fi
		fi
	else
		openwbDebugLog "CHARGESTAT" 2 "# skipping charge point $chargePointNumber (not configured)"
	fi
}

for i in {1..8}; do
	processChargepoint "$i"
done
