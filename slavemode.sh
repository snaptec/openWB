#!/bin/bash

openwbisslave() {
	AllowedTotalCurrentPerPhase=$(<ramdisk/AllowedTotalCurrentPerPhase)
	TotalCurrentConsumptionOnL1=$(<ramdisk/TotalCurrentConsumptionOnL1)
	ChargingVehiclesOnL1=$(<ramdisk/ChargingVehiclesOnL1)
	lldiff=$(( (AllowedTotalCurrentPerPhase - TotalCurrentConsumptionOnL1) / ChargingVehiclesOnL1))
	llneu=$(( llalt - lldiff))
	if (( llneu < minimalstromstaerke )); then
		llneu=0
	fi
	if (( llneu > maximalstromstaerke )); then
		llneu=$maximalstromstaerke
	fi
	runs/set-current.sh $llneu all
	if (( llalt != llneu )); then
		echo "$date Ändere Ladeleistung auf $llneu Ampere" >> ramdisk/ladestatus.log
	fi
	echo "Slave Mode Aktiv, openWB NUR fernsteuerbar" > ramdisk/lastregelungaktiv
	exit 0
}
