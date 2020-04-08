#!/bin/bash

HeartbeatTimeout=35
CurrentLimitAmpereForCpCharging=0.5
NumberOfSupportedChargePoints=2

#
# the main entry point of the script that is called from outside
openwbisslave() {

	# prepare for normal debug output in level 2, in others echo is the null command :
	dbgWrite=:
	if (( debug == 2 )); then
		dbgWrite=echo
	fi

	setVariablesFromRamdisk

	checkControllerHeartbeat

	for ((currentCp=1; currentCp<=NumberOfSupportedChargePoints; currentCp++)); do

		# we have to do a slightly ugly if-else-cascade to determine whether the currentCp is actually present
		# if not we continue the loop with the next CP
		if (( currentCp == 1)); then
			# CP1 exists unconditionally
			:
		elif (( currentCp == 2)) && (( lastmanagement == 0)); then
			# CP2 does not actually exist
			continue
		elif (( currentCp == 3)) && (( lastmanagements2 == 0)); then
			# CP3 does not actually exist
			continue
		elif (( currentCp >= 4)); then
			local cpPresentVar="lastmanagementlp${currentCp}"
			eval cpPresent=\$$cpPresentVar
			if (( cpPresent == 0 )); then

				# CPx (x >= 4) does not actually exist
				continue
			fi
		else
			echo "$NowItIs: Slave Mode charge point ERROR: Charge Point #${currentCp} is not supported"
			continue
		fi

		# handle the currentCp: first aggregate the data ...
		aggregateDataForChargePoint $currentCp

		# ... then calculate the new possible charge current
		computeAndSetCurrentForChargePoint $currentCp

	done

	echo "Slave Mode Aktiv, openWB NUR fernsteuerbar" > ramdisk/lastregelungaktiv

	exit 0
}

# actually computes the new allowed charge current for the given charge point
function computeAndSetCurrentForChargePoint() {

	# the charge point that we're looking at is our first parameter
	local chargePoint=$1

	declare -i chargingVehiclesAdjustedForThisCp=${ChargingVehiclesOnPhase[$ChargingPhaseWithMaximumTotalCurrent]}
	if !(( CpIsCharging )); then

		# add 1 for "ourself" as we need to calculate as if we were actually charging
		chargingVehiclesAdjustedForThisCp=$((chargingVehiclesAdjustedForThisCp+1))
	fi

	if (( chargingVehiclesAdjustedForThisCp == 0 )); then
		echo "$NowItIs: Slave Mode INTERNAL ERROR: chargingVehiclesAdjustedForThisCp == 0 - skipping slave loop for CP#${chargePoint} - is your CONTROLLER USING A TOO HIGH LIMIT FOR DETECTING CHARGING PHASES ??"
		return 1
	fi

	# compute difference between allowed current on the total current of the phase that has the highest total current and is actually used for charging
	# in floats for not to loos too much precision
	lldiff=$(echo "scale=3; ($AllowedTotalCurrentPerPhase - ${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent}) / ${chargingVehiclesAdjustedForThisCp}" | bc)

	# new charge current in int but always rounded to the next _lower_ integer
	llneu=$(echo "scale=0; ($llalt + $lldiff)/1" | bc)

	$dbgWrite "$NowItIs: Slave Mode: AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase, TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent}, chargingVehiclesAdjustedForThisCp=${chargingVehiclesAdjustedForThisCp}, llalt=$llalt, lldiff=$lldiff --> llneu=$llneu"

	# The llneu might exceed the AllowedTotalCurrentPerPhase if the EV doesn't actually start consuming
	# the allowed current (and hence TotalCurrentConsumptionOnL1 doesn't increase).
	# For this case we limit to the total allowed current divided by the number of charging vehicals.
	# The resulting value might get further limited to maximalstromstaerke below.
	if (( `echo "$llneu > $AllowedTotalCurrentPerPhase" | bc` == 1 )); then

		$dbgWrite "$NowItIs: Slave Mode: Special case: EV consuming less than allowed. Limiting to AllowedTotalCurrentPerPhase/ChargingVehicles"

		llneu=$(echo "scale=0; ($AllowedTotalCurrentPerPhase/${chargingVehiclesAdjustedForThisCp})" | bc)
	fi

	if (( llneu < minimalstromstaerke )) || ((LpEnabled == 0)); then
		if ((LpEnabled != 0)); then
			$dbgWrite "$NowItIs: Slave Mode Aktiv, LP akt., LpEnabled=$LpEnabled, llneu=$llneu < minmalstromstaerke=$minimalstromstaerke --> setze llneu=0"
		else
			$dbgWrite "$NowItIs: Slave Mode Aktiv, LP deakt. --> setze llneu=0"
		fi
		llneu=0
	fi
	if (( llneu > maximalstromstaerke )); then
		$dbgWrite "$NowItIs: Slave Mode Aktiv, llneu=$llneu < maximalstromstaerke=$maximalstromstaerke --> setze llneu=$maximalstromstaerke"
		llneu=$maximalstromstaerke
	fi

	callSetCurrent $llneu $chargePoint

	if (( llalt != llneu )); then
		echo "$date Ändere Ladeleistung von $llalt auf $llneu Ampere" >> ramdisk/ladestatus.log
	fi

	return 0
}


# determines the relevant phase for comparision against allowed current
# if we're charging on n phases we use the one with the highest total current reported by controller
# if we're not charging at all, we assume that we would start charging an 3 phases and thus use the
# highest of the total currents reported by controller
function aggregateDataForChargePoint() {

	# the charge point that we're looking at is our first parameter
	local chargePoint=$1

	# the per-phase currents (4 elements as index 0 will be ignored)
	ChargeCurrentOnPhase=(0 0 0 0)

	# the per-phase charge indicator (0 = not charging, 1 = charging)
	ChargingOnPhase=(0 0 0 0)

	# value indicating whether this CP is actually charging
	CpIsCharging=0

	ChargingPhaseWithMaximumTotalCurrent=0
	TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=0

	# indication whether the given charge point is actually enabled
	local cpenabledVar="lp${chargePoint}enabled"
	eval LpEnabled=\$$cpenabledVar

	# iterate the phases (index 1-3, index 0 of array will simply be untouched/ignored)
	for i in {1..3}; do

		# we have to do a slightly ugly if-else-cascade to determine the right ramdisk file name
		if (( chargePoint == 1 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/lla${i}")
		elif (( chargePoint == 2 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/llas1${i}")
		elif (( chargePoint == 3 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/llas2${i}")
		elif (( chargePoint >= 4 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/lla${i}lp${chargePoint}")
		else
			echo "$NowItIs: Slave Mode charge current fetch ERROR: Charge Point #${chargePoint} is not supported"
			return 1
		fi

		if (( `echo "${ChargeCurrentOnPhase[i]} > $CurrentLimitAmpereForCpCharging" | bc` == 1 )); then
			ChargingOnPhase[i]=1
			CpIsCharging=1

			if (( `echo "${TotalCurrentConsumptionOnPhase[i]} > $TotalCurrentOfChargingPhaseWithMaximumTotalCurrent" | bc` == 1 )); then
				TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=${TotalCurrentConsumptionOnPhase[i]}
				ChargingPhaseWithMaximumTotalCurrent=$i
			fi
		fi
	done

	# if we're not charging at all, use highest total current (assuming we would start charging on all 3 phases)
	if (( ChargingPhaseWithMaximumTotalCurrent == 0 )); then
		ChargingPhaseWithMaximumTotalCurrent=$PhaseWithMaximumTotalCurrent
		TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=$MaximumTotalCurrent
	fi

	$dbgWrite "$NowItIs: CP${chargePoint} (enabled=${LpEnabled}): ChargeCurrentOnPhase=${ChargeCurrentOnPhase[@]:1}, ChargingOnPhase=${ChargingOnPhase[@]:1}, charging phase with max total current = ${ChargingPhaseWithMaximumTotalCurrent} @ ${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent} A, CpIsCharging=${CpIsCharging}"

	return 0
}


# sets all the required variables from the ramdisk
# these are the values that are only relevant for slave mode - for other values we obviously rely on loadvars.sh
function setVariablesFromRamdisk() {

	# general use
	NowItIs=$(date +%s)

	# data from local control server
	AllowedTotalCurrentPerPhase=$(<ramdisk/AllowedTotalCurrentPerPhase)

	# phase with maximum current
	PhaseWithMaximumTotalCurrent=0
	MaximumTotalCurrent=0

	TotalCurrentConsumptionOnPhase=(0 0 0 0)
	ChargingVehiclesOnPhase=(0 0 0 0)
	for i in {1..3}
	do
		TotalCurrentConsumptionOnPhase[i]=$(<"ramdisk/TotalCurrentConsumptionOnL${i}")
		ChargingVehiclesOnPhase[i]=$(<"ramdisk/ChargingVehiclesOnL${i}")

		if (( `echo "${TotalCurrentConsumptionOnPhase[i]} > $MaximumTotalCurrent" | bc` == 1 )); then
			MaximumTotalCurrent=${TotalCurrentConsumptionOnPhase[i]}
			PhaseWithMaximumTotalCurrent=${i}
		fi
	done

	$dbgWrite "$NowItIs: TotalCurrentConsumptionOnPhase=${TotalCurrentConsumptionOnPhase[@]:1}, Phase with max total current = ${PhaseWithMaximumTotalCurrent} @ ${MaximumTotalCurrent} A"

	# heartbeat
	Heartbeat=$(<ramdisk/heartbeat)
	PreviousMaximumTotalCurrent=$(<ramdisk/PreviousMaximumTotalCurrent)
	IFS=',' read -ra previousTotalCurrentAndTimestampArray <<< "$PreviousMaximumTotalCurrent"
	heartbeatMissingFor=$(( NowItIs - previousTotalCurrentAndTimestampArray[1] ))

	return 0
}


# checks whether heartbeat from local control server is available
# if not, steps all charging immediately
# Heartbeat is always checked looking for regular change of total current reported by control server for phase #1
function checkControllerHeartbeat() {

	if [[ "${MaximumTotalCurrent}" == "${previousTotalCurrentAndTimestampArray[0]}" ]]; then
		$dbgWrite "$NowItIs: WARNING: Local Control Server Heartbeat: MaximumTotalCurrent (${MaximumTotalCurrent}) same as previous (${previousTotalCurrentAndTimestampArray[0]}) for $heartbeatMissingFor s (timeout $HeartbeatTimeout)"

		if (( heartbeatMissingFor > HeartbeatTimeout )); then
			if (( Heartbeat == 1 )) || (( debug == 2 )); then
				echo "$NowItIs: Slave Mode: HEARTBEAT ERROR: MaximumTotalCurrent (${MaximumTotalCurrent}) not changed by local control server for $heartbeatMissingFor > $HeartbeatTimeout seconds. STOP CHARGING IMMEDIATELY"
			fi
			echo "Slave Mode: Zentralserver Ausfall, Ladung auf allen LP deaktiviert !" > ramdisk/lastregelungaktiv
			echo "0" > ramdisk/heartbeat
			callSetCurrent 0 0
			exit 1
		else
			echo "1" > ramdisk/heartbeat
		fi
	else
		$dbgWrite "$NowItIs: MaximumTotalCurrent (${MaximumTotalCurrent}) different from previous (${previousTotalCurrentAndTimestampArray[0]}). Heartbeat OK after ${heartbeatMissingFor} s."

		if (( Heartbeat == 0 )); then
			echo "$NowItIs: Slave Mode: HEARTBEAT RETURNED: After $heartbeatMissingFor seconds"
		fi

		echo "${MaximumTotalCurrent},$NowItIs" > ramdisk/PreviousMaximumTotalCurrent
		echo "1" > ramdisk/heartbeat
	fi

	return 0
}


# calls "setCurrent" with correct parameters for given charge point
# needed because the charge point parameter of setCurrent is not a number but a string like m, s1, s2, lp4, lp...
function callSetCurrent() {

	# the new current to set is our first parameter
	declare -i -r currentToSet=$1

	# the charge point that we're looking at is the second parameter
	# numeric, value of 0 means "all"
	local chargePoint=$2

	# we have to do a slightly ugly if-else-cascade to set the charge point selector for set-current.sh
	if (( chargePoint == 0 )); then
		local chargePointString="all"
	elif (( chargePoint == 1 )); then
		local chargePointString="m"
	elif (( chargePoint == 2 )); then
		local chargePointString="s1"
	elif (( chargePoint == 3 )); then
		local chargePointString="s2"
	elif (( chargePoint >= 4 )); then
		local chargePointString="lp${chargePoint}"
	else
		echo "$NowItIs: Slave Mode charge current set ERROR: Charge Point #${chargePoint} is not supported"
		return 1
	fi

	$dbgWrite "$NowItIs: callSetCurrent(${currentToSet}, ${chargePoint}): Calling runs/set-current.sh ${currentToSet} ${chargePointString}"

	runs/set-current.sh $currentToSet "${chargePointString}"

	return 0
}
