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
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp4"; then
		runs/set-current.sh 0 lp4
		echo "$date LP4, Lademodus Stop. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp5"; then
		runs/set-current.sh 0 lp5
		echo "$date LP5, Lademodus Stop. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp6"; then
		runs/set-current.sh 0 lp6
		echo "$date LP6, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp7"; then
		runs/set-current.sh 0 lp7
		echo "$date LP7, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp8"; then
		runs/set-current.sh 0 lp8
		echo "$date LP8, Lademodus Stop. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if (( ladeleistung > 300 )); then
		runs/set-current.sh 0 m
		runs/set-current.sh 0 s1
		runs/set-current.sh 0 s2
		runs/set-current.sh 0 lp4
		runs/set-current.sh 0 lp5
		runs/set-current.sh 0 lp6
		runs/set-current.sh 0 lp7
		runs/set-current.sh 0 lp8

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
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp4"; then
		runs/set-current.sh 0 lp4
		echo "$date LP4, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp5"; then
		runs/set-current.sh 0 lp5
		echo "$date LP5, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp6"; then
		runs/set-current.sh 0 lp6
		echo "$date LP6, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp7"; then
		runs/set-current.sh 0 lp7
		echo "$date LP7, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuslp8"; then
		runs/set-current.sh 0 lp8
		echo "$date LP8, Lademodus Standby. Ladefreigabe noch aktiv. Stoppe Ladung" >> ramdisk/ladestatus.log
	fi

	exit 0
}
