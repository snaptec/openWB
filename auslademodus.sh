#!/bin/bash

auslademodus(){
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/set-current.sh 0 m
		echo "$date LP1, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
		runs/set-current.sh 0 s1
		echo "$date LP2, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
		runs/set-current.sh 0 s2
		echo "$date LP3, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log

	fi
	if (( llkombiniert > 300 )); then
		runs/set-current.sh 0 m
		runs/set-current.sh 0 s1
		runs/set-current.sh 0 s2
		echo "$date Alle Ladepunkte, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log

	fi
	exit 0
}

semiauslademodus(){
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/set-current.sh 0 m
		echo "$date LP1, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
		runs/set-current.sh 0 s1
		echo "$date LP2, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
		runs/set-current.sh 0 s2
		echo "$date LP3, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	exit 0
}
