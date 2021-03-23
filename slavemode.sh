#!/bin/bash

declare -r SlaveModeAllowedLoadImbalanceDefault=20.0
declare -r HeartbeatTimeout=35
declare -r CurrentLimitAmpereForCpCharging=0.5
declare -r LastChargingPhaseFile="ramdisk/lastChargingPhasesLp"
declare -r LastImbalanceFile="ramdisk/lastImbalanceLp"
declare -r ExpectedChangeFile="ramdisk/expectedChangeLp"
declare -r SocketActivatedFile="ramdisk/socketActivated"
declare -r SocketApprovedFile="ramdisk/socketApproved"
declare -r SocketRequestedFile="ramdisk/socketActivationRequested"
declare -r SystemVoltage=240
declare -r MaxCurrentOffset=1.0
declare -r LmStatusFile="ramdisk/lmStatusLp"
declare -r MinimumAdjustmentInterval=${slaveModeMinimumAdjustmentInterval:-15}
declare -r LmStatusSuperseded=0
declare -r LmStatusInLoop=1
declare -r LmStatusDownByLm=2
declare -r LmStatusDownByEv=3
declare -r LmStatusDownByError=4
declare -r LmStatusDownByDisable=5
declare -r LmStatusDownForSocket=8

if (( lastmanagement > 0 )); then
	declare -r -i NumberOfSupportedChargePoints=2
else
	declare -r -i NumberOfSupportedChargePoints=1
fi

#
# the main entry point of the script that is called from outside
openwbisslave() {

	setVariablesFromRamdisk

	checkControllerHeartbeat

	# socket mode, if either requested or already active,
	# otherwise normal EV charge mode
	if (( standardSocketInstalled > 0 )) && ( (( SocketActivationRequested > 0 )) || (( SocketActivated > 0 )) || (( SocketApproved > 0 )) ); then

		# socket slave mode
		openwbDebugLog "MAIN" 2 "Slave Socket mode: Checking: SocketActivationRequested == '${SocketActivationRequested}', SocketApproved == '${SocketApproved}', SocketActivated == '${SocketActivated}'"

		callSetCurrent 0 0  $LmStatusDownForSocket

		# handle de-activation request by socket or EV RFID scan
		if (( SocketActivationRequested >= 2 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode Socket: Socket DEactivation requested by socket or EV RFID tag scan. Socket will now be turned off."
			sudo python runs/standardSocket.py off
			echo 0 > $SocketRequestedFile

		# handle disapprove of active socket
		elif (( SocketActivated > 0 )) && (( SocketApproved == 0 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode Socket: Active socket disapproved by controller. Socket will now be turned off."
			echo "Slave Mode Socket: Active socket disapproved by controller. Socket will now be turned off."
			sudo python runs/standardSocket.py off

		# handle approved activation request
		elif (( SocketActivationRequested == 1 )) && (( SocketApproved == 1 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode Socket: Socket activation request has been approved by controller. Socket will now be turned on."
			sudo python runs/standardSocket.py on
			echo 0 > $SocketRequestedFile

		# handle explicit disapprove of activation
		elif ( (( SocketActivationRequested > 0 )) || (( SocketActivated > 0 )) ) && (( SocketApproved == 2 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode Socket: Socket activation has explicitly been DISapproved by controller."
			sudo python runs/standardSocket.py off
			echo 0 > $SocketRequestedFile
			echo 0 > $SocketApprovedFile

		# handle socket approval while we're not expecting it
		elif (( SocketActivationRequested == 0 )) && (( SocketActivated == 0 )) && (( SocketApproved > 0 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode Socket: Socket aproval while we're not expecting it. Restting the approval."
			echo 0 > $SocketRequestedFile
			echo 0 > $SocketApprovedFile

		# no change required
		else
			openwbDebugLog "MAIN" 0 "Slave Mode: Socket installed: No change required"
		fi

	else

		# EV slave mode
		for ((currentCp=1; currentCp<=NumberOfSupportedChargePoints; currentCp++)); do

			# we have to do a slightly ugly if-else-cascade to determine whether the currentCp is actually present
			# if not we continue the loop with the next CP
			if (( currentCp == 1)); then
				# CP1 exists unconditionally
				:
			elif (( currentCp == 2)) && (( lastmanagement == 0)); then
				# CP2 does not actually exist
				continue
			elif (( currentCp == 2)) && (( lastmanagement > 0)); then
				# CP2 does exist
				:
			elif (( currentCp == 3)) && (( lastmanagements2 == 0)); then
				# CP3 does not actually exist
				continue
			elif (( currentCp == 3)) && (( lastmanagements2 > 0)); then
				# CP3 does exist
				:
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
	fi

	echo "Slave Mode Aktiv, openWB NUR fernsteuerbar" > ramdisk/lastregelungaktiv

	# re-publish the state after control loop (in background)
	runs/pubmqtt.sh &

	exit 0
}

# actually computes the new allowed charge current for the given charge point
function computeAndSetCurrentForChargePoint() {

	# the charge point that we're looking at is our first parameter
	local chargePoint=$1

	# check if we're asked for a very fixed charge current (special cases superseding regular load management)
	# needed especially to allow additional cars a charge start
	if [ -f "ramdisk/FixedChargeCurrentCp${chargePoint}" ]; then
		local fixedCurrent=$(<"ramdisk/FixedChargeCurrentCp${chargePoint}")
		if (( fixedCurrent >= 0 )); then
			openwbDebugLog "MAIN" 2 "Slave Mode: Forced to ${fixedCurrent} A, ignoring imbalance"
			echo "0" > "${LastImbalanceFile}${chargePoint}"
			callSetCurrent $fixedCurrent $chargePoint $LmStatusSuperseded
			return 0
		fi
	fi

	# check if the car has done the adjustment that it has last been asked for
	local expectedChangeFile="${ExpectedChangeFile}${chargePoint}"
	local expectedChangeTimestamp=NowItIs
	local expectedCurrentPerPhase=-1
	if [ -f "${expectedChangeFile}" ]; then
		local expectedChangeContent=$(<"${expectedChangeFile}")
		IFS=',' read -ra expectedChangeArray <<< "$expectedChangeContent"
		expectedChangeTimestamp=${expectedChangeArray[0]}
		expectedCurrentPerPhase=${expectedChangeArray[1]}
		local timeSinceAdjustment=$(( NowItIs - expectedChangeTimestamp ))
		if (( timeSinceAdjustment < MinimumAdjustmentInterval )); then
			openwbDebugLog "MAIN" 2 "Slave Mode: Time after adjustment ${timeSinceAdjustment} < ${MinimumAdjustmentInterval} seconds. Skipping control loop"
			return 0
		fi
	fi

	# compute difference between allowed current on the total current of the phase that has the highest total current and is actually used for charging
	# in floats for not to loose too much precision
	local lldiff=$(echo "scale=3; ($AllowedTotalCurrentPerPhase - ${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent}) / ${ChargingVehiclesAdjustedForThisCp}" | bc)

	# limit this initial difference to the maximum allowed charge current of the charge point
	if (( `echo "$PreviousExpectedChargeCurrent + $lldiff > $MaximumCurrentPossibleForCp" | bc` == 1 )); then
		openwbDebugLog "MAIN" 2 "Slave Mode: PreviousExpectedChargeCurrent + lldiff > MaximumCurrentPossibleForCp ($PreviousExpectedChargeCurrent + $lldiff > $MaximumCurrentPossibleForCp): Limiting to MaximumCurrentPossibleForCp ($MaximumCurrentPossibleForCp)"
		lldiff=$(echo "scale=3; $MaximumCurrentPossibleForCp - ${PreviousExpectedChargeCurrent}" | bc)
	fi

	# see if we have to limit by allowed peak power (we have to if the value exists in ramdisk file and is > 0, ==0 means: peak limit disabled)
	if (( `echo "$AllowedPeakPower > 0" | bc` == 1 )); then

		if (( TotalPowerConsumption == -1 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode: ERROR: Peak power limit set (${AllowedPeakPower} W) but total power consumption not availble (TotalPowerConsumption=${TotalPowerConsumption} W): Immediately stopping charge and exiting"
			callSetCurrent 0 $chargePoint $LmStatusDownByError
			exit 2
		fi

		local pwrDiff=$(echo "scale=3; ($AllowedPeakPower - ${TotalPowerConsumption}) / ${ChargingVehiclesAdjustedForThisCp}" | bc)
		local pwrCurrDiff=$(echo "scale=3; (${pwrDiff} / ${SystemVoltage} / ${NumberOfChargingPhases})" | bc)

		if (( `echo "$pwrCurrDiff < $lldiff" | bc` == 1 )); then
			openwbDebugLog "MAIN" 2 "Slave Mode: Difference to power limt of $AllowedPeakPower W is $pwrDiff W (@ ${SystemVoltage} V @ ${ChargingVehiclesAdjustedForThisCp} charging vehicles) --> overriding $lldiff A to $pwrCurrDiff A on ${NumberOfChargingPhases} phase(s)"
			lldiff=$pwrCurrDiff
		fi
	fi

	openwbDebugLog "MAIN" 2 "Slave Mode: AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase A, AllowedPeakPower=${AllowedPeakPower} W, TotalPowerConsumption=${TotalPowerConsumption} W, before load imbalance compensation lldiff=${lldiff} A"

	# handle load imbalances - sets imbalDiff
	computeLoadImbalanceCompensation ${chargePoint} "${lldiff}"

	# final calculation of required adjustement
	lldiff=$(echo "scale=3; ($lldiff + $imbalDiff)" | bc)

	openwbDebugLog "MAIN" 2 "Slave Mode: AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase A, AllowedPeakPower=${AllowedPeakPower} W, TotalPowerConsumption=${TotalPowerConsumption} W, imbalDiff=${imbalDiff} A ==> lldiff=${lldiff}"

	# new charge current in int but always rounded to the next _lower_ integer
	llneu=$(echo "scale=0; ($PreviousExpectedChargeCurrent + $lldiff)/1" | bc)

	openwbDebugLog "MAIN" 2 "Slave Mode: TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent} A, ChargingVehiclesAdjustedForThisCp=${ChargingVehiclesAdjustedForThisCp}, PreviousExpectedChargeCurrent=$PreviousExpectedChargeCurrent A, lldiff=$lldiff A"

	# limit the change to +1, -1 or -3 if slow ramping is enabled,
	# a value of 0 will be kept unchanged
	if (( slaveModeSlowRamping == 1 )); then

		local adjustment=0;
		if (( `echo "$lldiff > 1.0" | bc` == 1 )); then
			adjustment=1
		elif (( `echo "$lldiff < -3.0" | bc` == 1 )); then
			adjustment=-3
		elif (( `echo "$lldiff < -0.5" | bc` == 1 )); then
			adjustment=-1
		fi

		if !(( CpIsCharging )); then
			# if we're not charging, we always start off with minimalstromstaerke
		if (( `echo "$lldiff < 0" | bc` == 1 )); then
				llneu=0
				openwbDebugLog "MAIN" 2 "Slave Mode: Slow ramping: Not charging: Too few current left to start"
			else
				llneu=${minimalstromstaerke}
				openwbDebugLog "MAIN" 2 "Slave Mode: Slow ramping: Not charging: Starting at minimal supported charge current ${llneu} A"
			fi
		else
			llneu=$(( PreviousExpectedChargeCurrent + adjustment ))
			openwbDebugLog "MAIN" 2 "Slave Mode: Slow ramping: Limiting adjustment to ${PreviousExpectedChargeCurrent} + (${adjustment}) --> llneu = ${llneu} A"
		fi
	else

		# In "fast" mode the llneu might exceed the AllowedTotalCurrentPerPhase if the EV doesn't actually start consuming
		# the allowed current (and hence TotalCurrentConsumptionOnL1 doesn't increase).
		# For this case we limit to the total allowed current divided by the number of charging vehicals.
		# The resulting value might get further limited to maximalstromstaerke below.
		if (( `echo "$llneu > $AllowedTotalCurrentPerPhase" | bc` == 1 )); then

			if (( $llneu > $PreviousExpectedChargeCurrent )); then
				openwbDebugLog "MAIN" 2 "Slave Mode: Fast ramping: EV seems to consume less than allowed (llneu=$llneu > AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase && llneu > PreviousExpectedChargeCurrent=$PreviousExpectedChargeCurrent): Not changing allowed current."
				llneu=$PreviousExpectedChargeCurrent
			else
				openwbDebugLog "MAIN" 2 "Slave Mode: Fast ramping: EV seems to consume less than allowed (llneu=$llneu > AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase && llneu <= PreviousExpectedChargeCurrent=$PreviousExpectedChargeCurrent): Limiting allowed current to $AllowedTotalCurrentPerPhase A."
				llneu=$AllowedTotalCurrentPerPhase
			fi
		else
			openwbDebugLog "MAIN" 2 "Slave Mode: Fast ramping: Setting llneu=$llneu A"
		fi
	fi

	callSetCurrent $llneu $chargePoint -1

	if (( PreviousExpectedChargeCurrent != llneu )); then
		echo "$date Ändere Ladeleistung von $PreviousExpectedChargeCurrent auf $llneu Ampere" >> ramdisk/ladestatus.log
	fi

	return 0
}

function computeLoadImbalanceCompensation() {

	# the charge point that we're looking at is our first parameter
	local chargePoint=$1
	local lldiff=$2

	# load imbalance handling
	local imbalPhase=$PhaseWithMaximumTotalCurrent
	local systemLoadImbalanceToUse=$SystemLoadImbalance

	local lastImbalance=0
	local lastImbalancePhase=$imbalPhase
	if [ -f "${LastImbalanceFile}${chargePoint}" ]; then
		lastImbalancePersistedValue=$(<${LastImbalanceFile}${chargePoint})
		IFS=',' read -ra lastImbalanceArray <<< $lastImbalancePersistedValue
		lastImbalance=${lastImbalanceArray[0]}
		lastImbalancePhase=${lastImbalanceArray[1]}
		openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: lastImbalancePersistedValue=$lastImbalancePersistedValue, lastImbalance=$lastImbalance, lastImbalancePhase=$lastImbalancePhase"
	fi

	# stick to last compensated phase
	if (( lastImbalancePhase > 0 )); then

		imbalPhase=$lastImbalancePhase
		systemLoadImbalanceToUse=$(echo "scale=3; (${TotalCurrentConsumptionOnPhase[$imbalPhase]} - ${TotalCurrentConsumptionOnPhase[$PhaseWithMinimumTotalCurrent]})" | bc)

		openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Sticking to previously reduced for imbalance on phase #${lastImbalancePhase} (@ ${TotalCurrentConsumptionOnPhase[$imbalPhase]} A) --> systemLoadImbalanceToUse=$systemLoadImbalanceToUse"
	else

		imbalPhase=$ChargingPhaseWithMaximumTotalCurrent
		systemLoadImbalanceToUse=$(echo "scale=3; (${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent} - ${TotalCurrentConsumptionOnPhase[$PhaseWithMinimumTotalCurrent]})" | bc)

		openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Using ChargingPhaseWithMaximumTotalCurrent=${ChargingPhaseWithMaximumTotalCurrent} @ ${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent} A and PhaseWithMinimumTotalCurrent=${PhaseWithMinimumTotalCurrent} @ ${TotalCurrentConsumptionOnPhase[$PhaseWithMinimumTotalCurrent]} A for imbalance calculation --> systemLoadImbalanceToUse=$systemLoadImbalanceToUse"
	fi

	imbalDiff=$(echo "scale=3; ($SlaveModeAllowedLoadImbalance - $systemLoadImbalanceToUse)" | bc)

	openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: lastImbalance=$lastImbalance, systemLoadImbalanceToUse=$systemLoadImbalanceToUse - SlaveModeAllowedLoadImbalance=$SlaveModeAllowedLoadImbalance = imbalDiff=${imbalDiff} A"

	#  have been compensating in last loop?                are we contributing ?                   we're not contributing to minimal current phase             is imbalance limit newly exceeded?
	if        (( lastImbalance < 0 ))         || ( (( ChargingOnPhase[$imbalPhase] == 1 )) && (( ChargingOnPhase[$PhaseWithMinimumTotalCurrent] == 0 )) && (( `echo "$imbalDiff < 0.0" | bc` == 1 )) ); then

		# we're contributing to imbalance and imbalance actually needs adjustment, first calculate our part of the contribution
		imbalDiff=$(echo "scale=3; ($imbalDiff / ${ChargingVehiclesOnPhase[$imbalPhase]})" | bc)

		openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: We're contributing! imbalPhase=$imbalPhase, ChargingVehiclesOnPhase[imbalPhase]=${ChargingVehiclesOnPhase[$imbalPhase]} ==> imbalDiff=${imbalDiff} A"

		# calculate new imbalance adjustement value in integer Ampere steps
		# Note: We need to do the rounding to next lower Ampere of imbalance in order to really enforce an adjustement.
		#       Using the float values might not trigger an adjustment immediately.
		if (( `echo "$imbalDiff < 0.0" | bc` == 1 )); then

			# newly calculated imbalance requires a reduction
			imbalDiff=$(echo "scale=0; ($lastImbalance + $imbalDiff - 0.9999)/1" | bc)

			openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Need to reduce current for imbalance compensation to imbalDiff=${imbalDiff} A"
		elif  (( `echo "$imbalDiff > 1.0" | bc` == 1 )); then

			# newly calculated imbalance allows more than 1 A more current
			imbalDiff=$(echo "scale=0; ($lastImbalance + $imbalDiff - 0.9999)/1" | bc)

			if (( PreviousExpectedChargeCurrent > 0)); then

				# EV was charging --> increase and disable normally
				if (( imbalDiff > 0 )) && (( PreviousExpectedChargeCurrent > 0)); then
					openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: No more limit contribution. Setting imbalDiff from ${imbalDiff} A to 0 A"
					imbalDiff=0
					imbalPhase=0
				else
					openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Can increase current even with imbalance compensation to imbalDiff=${imbalDiff} A"
				fi
			else

				# charging was stopped --> increase only if the minimum current for the EV is exceeded
				if (( `echo "$imbalDiff - $lastImbalance >= $minimalstromstaerke" | bc` == 1 )); then
					openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Stopped charging. Possible increase sufficient to re-start ($imbalDiff - $lastImbalance >= $minimalstromstaerke), setting imbalDiff=${imbalDiff} A"
				else
					imbalDiff=${lastImbalance}
					openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Stopped charging. Possible increase too low ($imbalDiff - $lastImbalance < $minimalstromstaerke), staying with imbalDiff=${imbalDiff} A"
				fi
			fi
		else

			# else we keep on using the previous imbalance
			imbalDiff=${lastImbalance}
			openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: No need to adjust imbalance compensation, keeping at lastImbalance as imbalDiff=${imbalDiff}"
		fi
	else

		# no imbalance compensation needed at all
		imbalDiff=0
		imbalPhase=0
		openwbDebugLog "MAIN" 2 "Slave Mode: Load Imbalance: Not contributing to imbalance (not charging on critical phase) or imbalance limit not hit ==> resetting compensation to 0"
	fi

	echo "${imbalDiff},${imbalPhase}" > "${LastImbalanceFile}${chargePoint}"
}

# determines the relevant phase for comparision against allowed current
# if we're charging on n phases we use the one with the highest total current reported by controller
# if we're not charging at all, we assume that we would start charging an 3 phases and thus use the
# highest of the total currents reported by controller
function aggregateDataForChargePoint() {

	# the charge point that we're looking at is our first parameter
	local chargePoint=$1

	# Note: There's currently only one current limit (min/max) per box - so setting same for all CPs
	MinimumCurrentPossibleForCp=$minimalstromstaerke
	MaximumCurrentPossibleForCp=$maximalstromstaerke
	# Note: Use the below commented code if we ever have different current limits per CP
	#if (( chargePoint == 1 )); then
	#	MinimumCurrentPossibleForCp=$minimalstromstaerke
	#	MaximumCurrentPossibleForCp=$maximalstromstaerke
	#elif (( chargePoint == 2 )); then
	#	MinimumCurrentPossibleForCp=$minimalstromstaerke
	#	MaximumCurrentPossibleForCp=$maximalstromstaerke
	#elif (( chargePoint == 3 )); then
	#	MinimumCurrentPossibleForCp=$minimalstromstaerke
	#	MaximumCurrentPossibleForCp=$maximalstromstaerke
	#elif (( chargePoint >= 4 )); then
	#	MinimumCurrentPossibleForCp=$minimalstromstaerke
	#	MaximumCurrentPossibleForCp=$maximalstromstaerke
	#else
	#	echo "$NowItIs: Slave Mode charge current set ERROR: Charge Point #${chargePoint} is not supported"
	#	return 1
	#fi

	# the per-phase currents (4 elements as index 0 will be ignored)
	ChargeCurrentOnPhase=(0 0 0 0)

	# the per-phase charge indicator (0 = not charging, 1 = charging)
	ChargingOnPhase=(0 0 0 0)

	# value indicating whether this CP is actually charging
	CpIsCharging=0

	ChargingPhaseWithMaximumTotalCurrent=0
	TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=0
	PreviousExpectedChargeCurrent=0

	# indication whether the given charge point is actually enabled
	local cpenabledVar="lp${chargePoint}enabled"
	eval LpEnabled=\$$cpenabledVar

	# iterate the phases (index 1-3, index 0 of array will simply be untouched/ignored)
	ChargingVehiclesAdjustedForThisCp=0
	local maxNumberOfChargingVehiclesAcrossAllPhases=0
	NumberOfChargingPhases=0
	for i in {1..3}; do

		# we have to do a slightly ugly if-else-cascade to determine the right ramdisk file name
		if (( chargePoint == 1 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/lla${i}")
			PreviousExpectedChargeCurrent=$llalt
		elif (( chargePoint == 2 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/llas1${i}")
			PreviousExpectedChargeCurrent=$llalts1
		elif (( chargePoint == 3 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/llas2${i}")
			PreviousExpectedChargeCurrent=$llalts2
		elif (( chargePoint >= 4 )); then
			ChargeCurrentOnPhase[i]=$(<"ramdisk/lla${i}lp${chargePoint}")
			PreviousExpectedChargeCurrent=$(<"ramdisk/ramdisk/llsolllp${chargePoint}")
		else
			openwbDebugLog "MAIN" 0 "Slave Mode charge current fetch ERROR: Charge Point #${chargePoint} is not supported"
			return 1
		fi

		# detect the phases on which WE are CURRENTLY charging and calculate dependent values
		if (( `echo "${ChargeCurrentOnPhase[i]} > $CurrentLimitAmpereForCpCharging" | bc` == 1 )); then
			ChargingOnPhase[i]=1
			CpIsCharging=1
			NumberOfChargingPhases=$(( NumberOfChargingPhases + 1 ))

			if (( `echo "${TotalCurrentConsumptionOnPhase[i]} > $TotalCurrentOfChargingPhaseWithMaximumTotalCurrent" | bc` == 1 )); then
				TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=${TotalCurrentConsumptionOnPhase[i]}
				ChargingPhaseWithMaximumTotalCurrent=$i
			fi

			if (( ChargingVehiclesOnPhase[i] > ChargingVehiclesAdjustedForThisCp )); then
				ChargingVehiclesAdjustedForThisCp=${ChargingVehiclesOnPhase[i]}
			fi
		fi

		if (( ChargingVehiclesOnPhase[i] > maxNumberOfChargingVehiclesAcrossAllPhases )); then
			maxNumberOfChargingVehiclesAcrossAllPhases=${ChargingVehiclesOnPhase[i]}
		fi
	done

	# write the phases on which we're currently charging to the ramdisk
	if (( CpIsCharging == 1 )); then
		local chargingOnPhaseString="${ChargingOnPhase[*]}"
		echo "${chargingOnPhaseString//${IFS:0:1}/,}" > "${LastChargingPhaseFile}${chargePoint}"
	fi

	# if we're not charging at all, try smart fallback first: use the phase(s) on which we have last charged
	if (( ChargingPhaseWithMaximumTotalCurrent == 0 )); then

		# check if "last charging phase" usage is enabled openwb.conf
		# if not right away skip to the ultimate fallback
		if (( slaveModeUseLastChargingPhase == 1)); then

			local previousChargingPhasesArray=(0 0 0 0)
			local previousNumberOfChargingPhases=0

			# get previously charging phases if available, else use all 0 (none)
			if [ -f "${LastChargingPhaseFile}${chargePoint}" ]; then
				previousChargingPhasesString=$(<"${LastChargingPhaseFile}${chargePoint}")
				IFS=',' read -ra previousChargingPhasesArray <<< "$previousChargingPhasesString"
			fi

			# iterate the phases and determine the last charging phase with maximum current
			# if no last charging phase, leaves variables unchagned (i.e. at their default of 0 to trigger ultimate fallback)
			for i in {1..3}; do

				if (( previousChargingPhasesArray[i] == 1 )); then

					previousNumberOfChargingPhases=$(( previousNumberOfChargingPhases + 1 ))

					if (( `echo "${TotalCurrentConsumptionOnPhase[i]} > $TotalCurrentOfChargingPhaseWithMaximumTotalCurrent" | bc` == 1 )); then
						TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=${TotalCurrentConsumptionOnPhase[i]}
						ChargingPhaseWithMaximumTotalCurrent=$i
					fi

					if (( ChargingVehiclesOnPhase[i] > ChargingVehiclesAdjustedForThisCp )); then
						ChargingVehiclesAdjustedForThisCp=${ChargingVehiclesOnPhase[i]}
					fi
				fi
			done
		else
			# not supposed to use last charging phase --> use maximum number of charging vehicles across all phases
			ChargingVehiclesAdjustedForThisCp=$maxNumberOfChargingVehiclesAcrossAllPhases
		fi

		# ultimate fallback: use phase with the highest total current
		# (i.e. assume we would start charging on all 3 phases)
		if (( ChargingPhaseWithMaximumTotalCurrent == 0 )); then
			openwbDebugLog "MAIN" 2 "CP${chargePoint}: Previously charging phase unknown or disabled. Using highst of all 3 phases for load management"
			ChargingPhaseWithMaximumTotalCurrent=$PhaseWithMaximumTotalCurrent
			TotalCurrentOfChargingPhaseWithMaximumTotalCurrent=$MaximumTotalCurrent
		else
			NumberOfChargingPhases=$previousNumberOfChargingPhases
			openwbDebugLog "MAIN" 2 "CP${chargePoint}: Previously charging phase #${ChargingPhaseWithMaximumTotalCurrent} has highest current and will be used for load management"
		fi
	fi

	# if we have no charging vehicles at all, assume ourself as charging (and avoid dev/0 error)
	if (( ChargingVehiclesAdjustedForThisCp == 0 )); then
		ChargingVehiclesAdjustedForThisCp=1
	fi

	# we must make sure that we don't leave NumberOfChargingPhases at 0 if we couldn't count it up to here
	# so we have to assume worst-case (charging on all three phases)
	if (( NumberOfChargingPhases == 0 )); then
		NumberOfChargingPhases=3
	fi

	openwbDebugLog "MAIN" 2 "CP${chargePoint} (enabled=${LpEnabled}): NumberOfChargingPhases=${NumberOfChargingPhases}, ChargeCurrentOnPhase=${ChargeCurrentOnPhase[@]:1}, ChargingOnPhase=${ChargingOnPhase[@]:1}, charging phase max total current = ${ChargingPhaseWithMaximumTotalCurrent} @ ${TotalCurrentOfChargingPhaseWithMaximumTotalCurrent} A, CpIsCharging=${CpIsCharging}, ChargingVehicles=${ChargingVehiclesOnPhase[@]:1}, ChargingVehiclesAdjustedForThisCp=${ChargingVehiclesAdjustedForThisCp}"

	return 0
}


# sets all the required variables from the ramdisk
# these are the values that are only relevant for slave mode - for other values we obviously rely on loadvars.sh
function setVariablesFromRamdisk() {

	# general use
	NowItIs=$(date +%s)

	# data from local control server - the total allowed current per phase ...
	# ... and optionally the Allowed Peak Power and the Total Power
	AllowedTotalCurrentPerPhase=$(<ramdisk/AllowedTotalCurrentPerPhase)
	if [ -f "ramdisk/AllowedPeakPower" ]; then
		AllowedPeakPower=$(<"ramdisk/AllowedPeakPower")
	else
		AllowedPeakPower=0
	fi
	if [ -f "ramdisk/TotalPower" ]; then
		TotalPowerConsumption=$(<ramdisk/TotalPower)
	else
		TotalPowerConsumption=-1
	fi
	if [ -f "ramdisk/SlaveModeAllowedLoadImbalance" ]; then
		SlaveModeAllowedLoadImbalance=$(<ramdisk/SlaveModeAllowedLoadImbalance)
	else
		SlaveModeAllowedLoadImbalance=${SlaveModeAllowedLoadImbalanceDefault}
	fi

	# phase with maximum current
	PhaseWithMaximumTotalCurrent=0
	PhaseWithMinimumTotalCurrent=0
	MaximumTotalCurrent=0
	MinimumTotalCurrent=999999

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

		if (( `echo "${TotalCurrentConsumptionOnPhase[i]} < $MinimumTotalCurrent" | bc` == 1 )); then
			MinimumTotalCurrent=${TotalCurrentConsumptionOnPhase[i]}
			PhaseWithMinimumTotalCurrent=${i}
		fi
	done

	SystemLoadImbalance=$(echo "scale=3; $MaximumTotalCurrent - $MinimumTotalCurrent" | bc)

	openwbDebugLog "MAIN" 2 "TotalCurrentConsumptionOnPhase=${TotalCurrentConsumptionOnPhase[@]:1}, Phase with max total current = ${PhaseWithMaximumTotalCurrent} @ ${MaximumTotalCurrent} A, min current = ${PhaseWithMinimumTotalCurrent} @ ${MinimumTotalCurrent} A, SlaveModeAllowedLoadImbalance=${SlaveModeAllowedLoadImbalance} A, current imbalance = ${SystemLoadImbalance} A"

	# heartbeat
	Heartbeat=$(<ramdisk/heartbeat)
	PreviousMaximumTotalCurrent=$(<ramdisk/PreviousMaximumTotalCurrent)
	IFS=',' read -ra previousTotalCurrentAndTimestampArray <<< "$PreviousMaximumTotalCurrent"
	heartbeatMissingFor=$(( NowItIs - previousTotalCurrentAndTimestampArray[1] ))

	if [ -f "$SocketRequestedFile" ]; then
		SocketActivationRequested=$(<"$SocketRequestedFile")
	else
		SocketActivationRequested=0
	fi

	if [ -f "$SocketActivatedFile" ]; then
		SocketActivated=$(<"$SocketActivatedFile")
	else
		SocketActivated=0
	fi

	if [ -f "$SocketApprovedFile" ]; then
		SocketApproved=$(<"$SocketApprovedFile")
	else
		SocketApproved=0
	fi

	return 0
}


# checks whether heartbeat from local control server is available
# if not, steps all charging immediately
# Heartbeat is always checked looking for regular change of total current reported by control server for phase #1
function checkControllerHeartbeat() {

	local comparisonValue="${MaximumTotalCurrent}"

	if [ -f "ramdisk/LastControllerPublish" ]; then
		comparisonValue=$(<"ramdisk/LastControllerPublish")
	fi

	if [[ "${comparisonValue}" == "${previousTotalCurrentAndTimestampArray[0]}" ]]; then
		openwbDebugLog "MAIN" 2 "WARNING: Local Control Server Heartbeat: Comparison value (${comparisonValue}) same as previous (${previousTotalCurrentAndTimestampArray[0]}) for $heartbeatMissingFor s (timeout $HeartbeatTimeout)"

		if (( heartbeatMissingFor > HeartbeatTimeout )); then
			if (( Heartbeat == 1 )) || (( debug == 2 )); then
				openwbDebugLog "MAIN" 0 "Slave Mode: HEARTBEAT ERROR: Comparison value (${comparisonValue}) not changed by local control server for $heartbeatMissingFor > $HeartbeatTimeout seconds. STOP CHARGING IMMEDIATELY"
			fi
			echo "Slave Mode: Zentralserver Ausfall, Ladung auf allen LP deaktiviert !" > ramdisk/lastregelungaktiv
			echo "0" > ramdisk/heartbeat
			callSetCurrent 0 0 $LmStatusDownByError
			if (( standardSocketInstalled > 0 )); then
				sudo python runs/standardSocket.py off
			fi
			exit 1
		else
			echo "1" > ramdisk/heartbeat
		fi
	else
		openwbDebugLog "MAIN" 2 "Comparison value (${comparisonValue}) different from previous (${previousTotalCurrentAndTimestampArray[0]}). Heartbeat OK after ${heartbeatMissingFor} s."

		if (( Heartbeat == 0 )); then
			openwbDebugLog "MAIN" 0 "Slave Mode: HEARTBEAT RETURNED: After $heartbeatMissingFor seconds"
		fi

		echo "${comparisonValue},$NowItIs" > ramdisk/PreviousMaximumTotalCurrent
		echo "1" > ramdisk/heartbeat
	fi

	return 0
}


# calls "setCurrent" with correct parameters for given charge point
# needed because the charge point parameter of setCurrent is not a number but a string like m, s1, s2, lp4, lp...
function callSetCurrent() {

	# the new current to set is our first parameter
	declare -i currentToSet=$1

	# the charge point that we're looking at is the second parameter
	# numeric, value of 0 means "all"
	local chargePoint=$2

	# the status reason to write to ramdisk
	local statusReason=$3
	local computedReason=$statusReason

	# we have to do a slightly ugly if-else-cascade to set the charge point selector for set-current.sh
	# Note: There's currently only one current limit (min/max) per box - so setting same for all CPs
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
		openwbDebugLog "MAIN" 0 "Slave Mode charge current set ERROR: Charge Point #${chargePoint} is not supported"
		return 1
	fi

	computedReason=$LmStatusInLoop

	# finally limit to the configured min or max values
	if ( (( currentToSet < MinimumCurrentPossibleForCp )) || ((LpEnabled == 0)) ) && (( currentToSet != 0 )); then
		if ((LpEnabled != 0)); then
			openwbDebugLog "MAIN" 2 "Slave Mode Aktiv, LP akt., LpEnabled=$LpEnabled, currentToSet=$currentToSet < MinimumCurrentPossibleForCp=$MinimumCurrentPossibleForCp --> setze currentToSet=0"
			computedReason=$LmStatusDownByLm
		else
			openwbDebugLog "MAIN" 2 "Slave Mode Aktiv, LP deakt. --> setze currentToSet=0"
			computedReason=$LmStatusDownByDisable
		fi
		currentToSet=0
	fi

	if (( currentToSet > MaximumCurrentPossibleForCp )); then
		openwbDebugLog "MAIN" 2 "Slave Mode Aktiv, currentToSet=$currentToSet < MaximumCurrentPossibleForCp=$MaximumCurrentPossibleForCp --> setze currentToSet=$MaximumCurrentPossibleForCp"
		currentToSet=$MaximumCurrentPossibleForCp
	fi

	if (( PreviousExpectedChargeCurrent != currentToSet )); then

		openwbDebugLog "MAIN" 2 "Setting current to ${currentToSet} A for CP#${chargePoint}"
		echo "$NowItIs,$currentToSet" > "${ExpectedChangeFile}${chargePoint}"
	fi

	if (( $statusReason == -1 )); then
		if (( $CpIsCharging == 1 )) || (( $currentToSet == 0 )); then
			statusReason=$computedReason
		else
			statusReason=$LmStatusDownByEv
		fi
	fi

	openwbDebugLog "MAIN" 2 "Settings status reason = $statusReason"

	if (( chargePoint != 0 )); then
		echo "$statusReason" > "${LmStatusFile}${chargePoint}"
	else
		for i in $(seq 1 $NumberOfSupportedChargePoints);
		do
			echo "$statusReason" > "${LmStatusFile}${i}"
		done
	fi

	runs/set-current.sh $currentToSet "${chargePointString}"

	return 0
}
