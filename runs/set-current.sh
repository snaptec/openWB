#!/bin/bash

#####
#
# File: set-current.sh
#
# Copyright 2018 David Meder-Marouelli
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####

# set charging current in EVSE
#
# Parameters:
# 1: current
# 2: charging points, one of "all","m","s1","s2"
#
# Example: ./set-current.sh 9 s1
# sets charging current on point "s1" to 9A

. /var/www/html/openWB/openwb.conf

#####
#
# functions
# 
#####

# function for setting the current - dac
# Parameters:
# 1: current
# 2: dacregister
function setChargingCurrentDAC () {
	current=$1
	dacregister=$2
	# set desired charging current 
	# TODO: update dac.py to accept current and use translation table 
	sudo python /var/www/html/openWB/runs/dac.py 1298 $dacregister
}

# function for setting the current - modbusevse
# Parameters:
# 1: current
# 2: modbusevseresource
# 3: modbusevseid
function setChargingCurrentModbus () {
	current=$1
	modbusevsesource=$2
	modbusevseid=$3
	# set desired charging current
	sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid $current
}

# function for setting the current - WiFi
# Parameters:
# 1: current
# 2: evsewifitimeoutlp1 
# 3: evsewifiiplp1
function setChargingCurrentWifi () {
	if [[ $evsecon == "simpleevsewifi" ]]; then
		output=$(curl --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/getParameters)
		state=$(echo $output | jq '.list[] | .evseState')
		if ((state == false)) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setStatus?active=true > /dev/null
		fi
		oldcurrent=$(echo $output | jq '.list[] | .actualCurrent')
		if (( oldcurrent != $current )) ; then
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setCurrent?current=$current > /dev/null
		fi
	fi
}

# function for setting the charging current
# no parameters, variables need to be set before...
function setChargingCurrent () {
	if [[ $evsecon == "dac" ]]; then
		setChargingCurrentDAC $current $dacregister
	fi

	if [[ $evsecon == "modbusevse" ]]; then
		setChargingCurrentModbus $current $modbusevsesource $modbusevseid 
	fi

	if [[ $evsecon == "simpleevsewifi" ]]; then
		setChargingCurrentWifi $current $evsewifitimeoutlp1 $evsewifiiplp1
	fi
}

#####
#
# main routine 
#
#####

# input validation
let current=$1
if [[ current -le 0 ]] | [[ current -ge 32 ]]; then 
	if [[ $debug == "2" ]]; then 
		echo "ungültiger Wert für Ladestrom" > /var/www/html/openWB/web/lade.log
	fi
	exit 1
fi

if !([[ $2 == "all" ]] || [[ $2 == "m" ]] || [[ $2 == "s1" ]] || [[ $2 == "s2" ]]) ; then
	if [[ $debug == "2" ]]; then
		echo "ungültiger Wert für Ziel: $2" > /var/www/html/openWB/web/lade.log
	fi
	exit 1
fi

# value below threshold
if [[ current -le 7 ]]; then 
	if [[ $debug == "2" ]]; then 
		echo "Ladestrom < 7A, setze auf 0A"
	fi
	# TODO: Code for 0A charging current, i.e. turn off charging
	exit 0
fi 

# set desired charging current 

if [[ $debug == "2" ]]; then
	echo "setze ladung auf $current" >> /var/www/html/openWB/web/lade.log
fi

# set charging current - first charging point
if [[ $2 == "all" ]] || [[ $2 == "m" ]]; then
	setChargingCurrent
	echo 10 > /var/www/html/openWB/ramdisk/llsoll
	echo 1 > /var/www/html/openWB/ramdisk/ladestatus
fi

# set charging current - second charging point
if [[ $lastmanagement == "1" & ]]; then
	if [[ $2 == "all" ]] || [[ $2 == "s1" ]]; then
		evsecon=$evsecons1
		dacregister=$dacregisters1
		modbusevsesource=$evsesources1
		modbusevseid=$evseids1
		evsewifitimeoutlp1=$evsewifitimeoutlp2
		evsewifiiplp1=$evsewifiiplp2

		# dirty call (no parameters, all is set above...)
		setChargingCurrent

		echo 10 > /var/www/html/openWB/ramdisk/llsolls1
		echo 1 > /var/www/html/openWB/ramdisk/ladestatuss1
	fi
fi

# set charging current - second charging point
if [[ $lastmanagements2 == "1" ]]; then
	if [[ $2 == "all" ]] || [[ $2 == "s2" ]]; then 
		evsecon=$evsecons2
		dacregister=$dacregisters2
		modbusevsesource=$evsesources2
		modbusevseid=$evseids2
		evsewifitimeoutlp1=$evsewifitimeoutlp3
		evsewifiiplp1=$evsewifiiplp3

		# dirty call (no parameters, all is set above...)
		setChargingCurrent

		echo 1 > /var/www/html/openWB/ramdisk/ladestatuss2
		echo 10 > /var/www/html/openWB/ramdisk/llsolls2
	fi
fi
