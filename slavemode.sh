#!/bin/bash

HeartbeatTimeout=35

openwbisslave() {
	AllowedTotalCurrentPerPhase=$(<ramdisk/AllowedTotalCurrentPerPhase)
	TotalCurrentConsumptionOnL1=$(<ramdisk/TotalCurrentConsumptionOnL1)
	ChargingVehiclesOnL1=$(<ramdisk/ChargingVehiclesOnL1)
	Heartbeat=$(<ramdisk/heartbeat)
	NowItIs=$(date +%s)

	# check heartbeat
	PreviousTotalCurrentConsumptionOnL1=$(<ramdisk/PreviousTotalCurrentConsumptionOnL1)
	IFS=',' read -ra previousTotalCurrentAndTimestampArray <<< "$PreviousTotalCurrentConsumptionOnL1"
	heartbeatMissingFor=$(( NowItIs - previousTotalCurrentAndTimestampArray[1] ))
	if [[ "$TotalCurrentConsumptionOnL1" == "${previousTotalCurrentAndTimestampArray[0]}" ]]; then
		if (( debug == 2 )); then
			echo "$NowItIs: WARNING: Local Control Server Heartbeat: TotalCurrentConsumptionOnL1 ($TotalCurrentConsumptionOnL1) same as previous (${previousTotalCurrentAndTimestampArray[0]}) for $heartbeatMissingFor s (timeout $HeartbeatTimeout)"
		fi

		if (( heartbeatMissingFor > HeartbeatTimeout )); then
			if (( Heartbeat == 1 )) || (( debug == 2 )); then
				echo "$NowItIs: Slave Mode: HEARTBEAT ERROR: TotalCurrentConsumptionOnL1 ($TotalCurrentConsumptionOnL1) not changed by local control server for $heartbeatMissingFor > $HeartbeatTimeout seconds. STOP CHARGING IMMEDIATELY"
			fi
			echo "0" > ramdisk/heartbeat
			runs/set-current.sh 0 all
			exit 0
		else
			echo "1" > ramdisk/heartbeat
		fi
	else
		if (( debug == 2 )); then
			echo "$NowItIs: TotalCurrentConsumptionOnL1 ($TotalCurrentConsumptionOnL1) different from previous (${previousTotalCurrentAndTimestampArray[0]}). Heartbeat OK after ${heartbeatMissingFor} s."
		fi
		if (( Heartbeat == 0 )); then
			echo "$NowItIs: Slave Mode: HEARTBEAT RETURNED: After $heartbeatMissingFor seconds"
		fi
		echo "${TotalCurrentConsumptionOnL1},$NowItIs" > ramdisk/PreviousTotalCurrentConsumptionOnL1
		echo "1" > ramdisk/heartbeat
	fi

	# if no EV's are charging at all it would be a div/0
	# but also from logical point of view: we have to assume at least ourself as "charging"
	if [ "$ChargingVehiclesOnL1" -eq "0" ]; then
		ChargingVehiclesOnL1=1
	fi

	# compute difference in floats for not to loos too much precision
	lldiff=$(echo "scale=3; ($AllowedTotalCurrentPerPhase - $TotalCurrentConsumptionOnL1) / $ChargingVehiclesOnL1" | bc)

	# new charge current in int but always rounded to the next _lower_ integer
	llneu=$(echo "scale=0; ($llalt + $lldiff)/1" | bc)

	# The llneu might exceed the AllowedTotalCurrentPerPhase if the EV doesn't actually start consuming
	# the allowed current (and hence TotalCurrentConsumptionOnL1 doesn't increase).
	# For this case we limit to the total allowed current divided by the number of charging vehicals.
	# The resulting value might get further limited to maximalstromstaerke below.
	if (( `echo "$llneu > $AllowedTotalCurrentPerPhase" | bc` == 1 )); then
	        if (( debug == 2 )); then
			echo "$NowItIs: Slave Mode: Special case: EV consuming less than allowed. Limiting to AllowedTotalCurrentPerPhase/ChargingVehicles"
	        fi
	        llneu=$(echo "scale=0; ($AllowedTotalCurrentPerPhase/$ChargingVehiclesOnL1)" | bc)
	fi

	if (( debug == 2 )); then
		echo "$NowItIs: Slave Mode: AllowedTotalCurrentPerPhase=$AllowedTotalCurrentPerPhase, TotalCurrentConsumptionOnL1=$TotalCurrentConsumptionOnL1, ChargingVehiclesOnL1=$ChargingVehiclesOnL1, llalt=$llalt, lldiff=$lldiff --> llneu=$llneu"
	fi

	if (( llneu < minimalstromstaerke )) || ((lp1enabled == 0)); then
		if ((lp1enabled != 0)) && (( debug == 2 )); then
			echo "Slave Mode Aktiv, LP akt., lp1enabled=$lp1enabled, llneu=$llneu < minmalstromstaerke=$minimalstromstaerke --> setze llneu=0"
		fi
		if ((lp1enabled == 0)) && (( debug == 2 )); then
			echo "Slave Mode Aktiv, LP deakt. --> setze llneu=0"
		fi
		llneu=0
	fi
	if (( llneu > maximalstromstaerke )); then
		if (( debug == 2 )); then
			echo "Slave Mode Aktiv, llneu=$llneu < maximalstromstaerke=$maximalstromstaerke --> setze llneu=$maximalstromstaerke"
		fi
		llneu=$maximalstromstaerke
	fi

	runs/set-current.sh $llneu all

	if (( llalt != llneu )); then
		echo "$date Ändere Ladeleistung von $llalt auf $llneu Ampere" >> ramdisk/ladestatus.log
	fi

	echo "Slave Mode Aktiv, openWB NUR fernsteuerbar" > ramdisk/lastregelungaktiv

	exit 0
}
