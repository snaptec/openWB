#!/bin/bash
#####
#
# File: set-current.sh
#
# Copyright 2018 David Meder-Marouelli, Kevin Wieland
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

lp1enabled=$(<ramdisk/lp1enabled)
lp2enabled=$(<ramdisk/lp2enabled)
lp3enabled=$(<ramdisk/lp3enabled)
lp4enabled=$(<ramdisk/lp4enabled)
lp5enabled=$(<ramdisk/lp5enabled)
lp6enabled=$(<ramdisk/lp6enabled)
lp7enabled=$(<ramdisk/lp7enabled)
lp8enabled=$(<ramdisk/lp8enabled)
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
	# INFO: needs new dac.py to accept current and use translation table
	sudo python /var/www/html/openWB/runs/dac.py $current $dacregister
}

# function for setting the current - extopenwb
# Parameters:
# 1: current
# 2: chargep1ip
function setChargingCurrentExtopenwb () {
	current=$1
	chargep1ip=$2
	chargep1cp=$3
	# set desired charging current
	if [[ "$chargep1cp" == "2" ]]; then
		mosquitto_pub -r -t openWB/set/isss/Lp2Current -h $chargep1ip -m "$current"
	else
		mosquitto_pub -r -t openWB/set/isss/Current -h $chargep1ip -m "$current"
	fi
}

# function for setting the current - owbpro
# Parameters:
# 1: current
# 2: owbpro1ip

function setChargingCurrentOwbpro () {
	current=$1
	owbpro1ip=$2
	# set desired charging current
	curl -s -X POST --data "ampere=$current" $owbpro1ip/connect.php > /dev/null
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

function setChargingCurrentBuchse () {
	current=$1
	# set desired charging current
	#sudo python /var/www/html/openWB/runs/evsewritemodbus.py $modbusevsesource $modbusevseid $current
	# Is handled in buchse.py
}
function setChargingCurrentDaemon () {
	current=$1
	# set desired charging current
	# Is handled in lldaemon.py
}
# function for setting the current - IP modbusevse
# Parameters:
# 1: current
# 2: evseip
# 3: modbusevseid
function setChargingCurrentIpModbus () {
	current=$1
	evseip=$2
	ipevseid=$3
	# set desired charging current
	sudo python /var/www/html/openWB/runs/evseipwritemodbus.py $current $evseip $ipevseid
}

# function for openwb slave kit
function setChargingCurrentSlaveeth () {
	current=$1
	# set desired charging current
	sudo python /var/www/html/openWB/runs/evseslavewritemodbus.py $current
}

function setChargingCurrentMasterethframer () {
	current=$1
	# set desired charging current
	sudo python /var/www/html/openWB/runs/evsemasterethframerwritemodbus.py $current
}

# function for openwb third kit
function setChargingCurrentThirdeth () {
	current=$1
	# set desired charging current
	sudo python /var/www/html/openWB/runs/evsethirdwritemodbus.py $current
}

# function for setting the current - WiFi
# Parameters:
# 1: current
# 2: evsewifitimeoutlp1
# 3: evsewifiiplp1
function setChargingCurrentWifi () {
	if [[ $evsecon == "simpleevsewifi" ]]; then
		if [[ $evsewifitimeoutlp1 -eq 4 ]]; then
			if [[ $current -eq 0 ]]; then
				output=$(curl --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/getParameters)
				state=$(echo $output | jq '.list[] | .evseState')
				if ((state == true)) ; then
					curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setStatus?active=false > /dev/null
				fi
			else
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
		else
			curl --silent --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/setCurrent?current=$current > /dev/null
		fi
	fi
}

function setChargingCurrenttwcmanager () {
	if [[ $evsecon == "twcmanager" ]]; then
		if [[ $twcmanagerlp1httpcontrol -eq 1 ]]; then
			if [[ $current -eq 0 ]]; then
				curl -s --connect-timeout 3 -X POST -d '' "http://$twcmanagerlp1ip:$twcmanagerlp1port/api/cancelChargeNow" > /dev/null
			else
				curl -s --connect-timeout 3 -X POST -d '{ "chargeNowRate": '$current', "chargeNowDuration": 86400 }' "http://$twcmanagerlp1ip:$twcmanagerlp1port/api/chargeNow" > /dev/null
			fi
		else
			curl -s --connect-timeout 3 "http://$twcmanagerlp1ip/index.php?&nonScheduledAmpsMax=$current&submit=Save" > /dev/null
		fi
	fi
}

function setChargingCurrenthttp () {
	if [[ $evsecon == "httpevse" ]]; then
		curl -s --connect-timeout 3 "http://$httpevseip/setcurrent?current=$current" > /dev/null
	fi
}

# function for setting the current - go-e charger
# Parameters:
# 1: current
# 2: goetimeoutlp1
# 3: goeiplp1
function setChargingCurrentgoe () {
	if [[ $evsecon == "goe" ]]; then
		if [[ $current -eq 0 ]]; then
			output=$(curl --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/status)
			state=$(echo $output | jq -r '.alw')
			if ((state == "1")) ; then
				curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=alw=0 > /dev/null
			fi
		else
			output=$(curl --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/status)
			fwv=$(echo $output | jq -r '.fwv' | grep -Po "[1-9]\d{1,2}")
			state=$(echo $output | jq -r '.alw')
			if ((state == "0")) ; then
				 curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=alw=1 > /dev/null
			fi
			oldgoecurrent=$(echo $output | jq -r '.amp')
			if (( oldgoecurrent != $current )) ; then
				if (($fwv >= 40)) ; then
					curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=amx=$current > /dev/null
				else
					curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=amp=$current > /dev/null
				fi
			fi
		fi
	fi
}

# function for setting the current - keba charger
# Parameters:
# 1: current
# 2: goeiplp1
function setChargingCurrentkeba () {
	if [[ $evsecon == "keba" ]]; then
		sudo python3 /var/www/html/openWB/modules/keballlp1/check502.py $kebaiplp1 >> /var/www/html/openWB/ramdisk/port.log 2>&1
		modbus=$(</var/www/html/openWB/ramdisk/port_502_$kebaiplp1 )
		if [[ $modbus == "0" ]] ; then
			#modbus 0 means udp interface
			kebacurr=$(( current * 1000 ))
			if [[ $current -eq 0 ]]; then
				echo -n "ena 0" | socat - UDP-DATAGRAM:$kebaiplp1:7090
			else
				echo -n "ena 1" | socat - UDP-DATAGRAM:$kebaiplp1:7090
				echo -n "curr $kebacurr" | socat - UDP-DATAGRAM:$kebaiplp1:7090
				echo -n "display 1 10 10 0 S$current" | socat - UDP-DATAGRAM:$kebaiplp1:7090
			fi
		else
			#modbus 1 means modbus interface 
			sudo python3 /var/www/html/openWB/modules/keballlp1/setcurrkeba.py $kebaiplp1 $current >> /var/www/html/openWB/ramdisk/port.log 2>&1
		fi
	fi
}

function setChargingCurrentnrgkick () {
	if [[ $evsecon == "nrgkick" ]]; then
		if [[ $current -eq 0 ]]; then
			output=$(curl --connect-timeout 3 -s http://$nrgkickiplp1/api/settings/$nrgkickmaclp1)
			state=$(echo $output | jq -r '.Values.ChargingStatus.Charging')
			if [[ $state == "true" ]] ; then
				curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": false }, "ChargingCurrent": { "Value": "6" }, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
			fi
		else
			output=$(curl --connect-timeout 3 -s http://$nrgkickiplp1/api/settings/$nrgkickmaclp1)
			state=$(echo $output | jq -r '.Values.ChargingStatus.Charging')
			if [[ $state == "false" ]] ; then
				 curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current }, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
			fi
			oldcurrent=$(echo $output | jq -r '.Values.ChargingCurrent.Value')
			if (( oldcurrent != $current )) ; then
				curl --silent --connect-timeout $nrgkicktimeoutlp1 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current}, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
 > /dev/null
			fi
		fi
	fi
}

# function for setting the charging current
# no parameters, variables need to be set before...
function setChargingCurrent () {
	if [[ $evsecon == "dac" ]]; then
		setChargingCurrentDAC $current $dacregister
	fi
	if [[ $evsecon == "buchse" ]]; then
		setChargingCurrentBuchse $current
	fi
	if [[ $evsecon == "daemon" ]]; then
		setChargingCurrentDaemon $current
	fi
	if [[ $evsecon == "http" ]]; then
		setChargingCurrenthttp $current
	fi
	if [[ $evsecon == "extopenwb" ]]; then
		setChargingCurrentExtopenwb $current $chargep1ip $chargep1cp
	fi
	if [[ $evsecon == "owbpro" ]]; then
		setChargingCurrentOwbpro $current $owbpro1ip
	fi
	if [[ $evsecon == "modbusevse" ]]; then
		if [[ "$modbusevseid" == 0 ]]; then
			if [ -f /var/www/html/openWB/ramdisk/evsemodulconfig ]; then
				modbusevsesource=$(<ramdisk/evsemodulconfig)
				modbusevseid=1

			else
				if [ -f /dev/ttyUSB0 ]; then
					echo "/dev/ttyUSB" > ramdisk/evsemodulconfig
				else
					echo "/dev/serial0" > ramdisk/evsemodulconfig
				fi
				modbusevsesource=$(<ramdisk/evsemodulconfig)
				modbusevseid=1

			fi
		fi

		setChargingCurrentModbus $current $modbusevsesource $modbusevseid
	fi

	if [[ $evsecon == "simpleevsewifi" ]]; then
		setChargingCurrentWifi $current $evsewifitimeoutlp1 $evsewifiiplp1
	fi
	if [[ $evsecon == "goe" ]]; then
		setChargingCurrentgoe $current $goetimeoutlp1 $goeiplp1
	fi
	if [[ $evsecon == "slaveeth" ]]; then
		setChargingCurrentSlaveeth $current
	fi
	if [[ $evsecon == "thirdeth" ]]; then
		setChargingCurrentThirdeth $current
	fi

	if [[ $evsecon == "masterethframer" ]]; then
		setChargingCurrentMasterethframer $current
	fi
	if [[ $evsecon == "nrgkick" ]]; then
		setChargingCurrentnrgkick $current $nrgkicktimeoutlp1 $nrgkickiplp1 $nrgkickmaclp1 $nrgkickpwlp1
	fi
	if [[ $evsecon == "keba" ]]; then
		setChargingCurrentkeba $current $kebaiplp1
	fi
	if [[ $evsecon == "twcmanager" ]]; then
		setChargingCurrenttwcmanager $current $twcmanagerlp1ip $twcmanagerlp1port $twcmanagerlp1httpcontrol
	fi
	if [[ $evsecon == "ipevse" ]]; then
		setChargingCurrentIpModbus $current $evseip $ipevseid
	fi
}

#####
#
# main routine
#
#####

# input validation
let current=$1
if [[ current -lt 0 ]] | [[ current -gt 32 ]]; then
	if [[ $debug == "2" ]]; then
		echo "ungültiger Wert für Ladestrom" > /var/www/html/openWB/web/lade.log
	fi
	exit 1
fi

if !([[ $2 == "all" ]] || [[ $2 == "m" ]] || [[ $2 == "s1" ]] || [[ $2 == "s2" ]] || [[ $2 == "lp4" ]] || [[ $2 == "lp5" ]] || [[ $2 == "lp6" ]] || [[ $2 == "lp7" ]] || [[ $2 == "lp8" ]]) ; then
	if [[ $debug == "2" ]]; then
		echo "ungültiger Wert für Ziel: $2" > /var/www/html/openWB/web/lade.log
	fi
	exit 1
fi

# value below threshold
if [[ current -lt 6 ]]; then
	if [[ $debug == "2" ]]; then
		echo "Ladestrom < 6A, setze auf 0A"
	fi
	current=0
	lstate=0
else
	lstate=1
fi

# set desired charging current

if [[ $debug == "2" ]]; then
	echo "setze ladung auf $current" >> /var/www/html/openWB/web/lade.log
fi

# Loadsharing LP 1 / 2
if [[ $loadsharinglp12 == "1" ]]; then
	if (( loadsharingalp12 == 16 )); then
		agrenze=8
		aagrenze=16
		if (( current > 16 )); then
			current=16
			new2=all
		fi
	else
		agrenze=16
		aagrenze=32
	fi
	if (( current > agrenze )); then
		lla1=$(cat /var/www/html/openWB/ramdisk/lla1)
		lla2=$(cat /var/www/html/openWB/ramdisk/lla2)
		lla3=$(cat /var/www/html/openWB/ramdisk/lla3)
		lla1=$(echo $lla1 | sed 's/\..*$//')
		lla2=$(echo $lla2 | sed 's/\..*$//')
		lla3=$(echo $lla3 | sed 's/\..*$//')
		llas11=$(cat /var/www/html/openWB/ramdisk/llas11)
		llas12=$(cat /var/www/html/openWB/ramdisk/llas12)
		llas13=$(cat /var/www/html/openWB/ramdisk/llas13)
		llas11=$(echo $llas11 | sed 's/\..*$//')
		llas12=$(echo $llas12 | sed 's/\..*$//')
		llas13=$(echo $llas13 | sed 's/\..*$//')
		lslpl1=$((lla1 + llas12))
		lslpl2=$((lla2 + llas13))
		lslpl3=$((lla3 + llas11))
		#detect charging cars
		if (( lla1 > 1 )); then
			lp1c=1
			if (( lla2 > 1 )); then
				lp1c=2
			fi
		else
			lp1c=0
		fi
		if (( llas11 > 1 )); then
			lp2c=1
			if (( llas12 > 1 )); then
				lp2c=2
			fi
		else
			lp2c=0
		fi
		chargingphases=$(( lp1c + lp2c ))
		if (( chargingphases > 2 )); then
			current=$agrenze
		fi
		if (( lslpl1 > aagrenze )) && (( lslpl2 > aagrenze )) && (( lslpl3 > aagrenze )); then
			current=$(( agrenze - 1))
			new2=all
			if [[ $debug == "2" ]]; then
			echo "setzeladung auf $current durch loadsharing LP12" >> /var/www/html/openWB/web/lade.log
			fi
		fi
	fi
fi


if ! [ -z $new2 ]; then
	points=$new2
else
	points=$2
fi

# set charging current - first charging point
if [[ $points == "all" ]] || [[ $points == "m" ]]; then
		evseip=$evseiplp1
		ipevseid=$evseidlp1

	if (( lp1enabled == 0 )); then
		oldcurrent=$current
		current=0
	fi
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsoll
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatus
	if (( lp1enabled == 0 )); then
		current=$oldcurrent
	fi


fi

# set charging current - second charging point
if [[ $lastmanagement == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "s1" ]]; then
		evsecon=$evsecons1
		dacregister=$dacregisters1
		modbusevsesource=$evsesources1
		modbusevseid=$evseids1
		evsewifitimeoutlp1=$evsewifitimeoutlp2
		evsewifiiplp1=$evsewifiiplp2
		goeiplp1=$goeiplp2
		goetimeoutlp1=$goetimeoutlp2
		kebaiplp1=$kebaiplp2
		nrgkickiplp1=$nrgkickiplp2
		nrgkicktimeoutlp1=$nrgkicktimeoutlp2
		nrgkickmaclp1=$nrgkickmaclp2
		nrgkickpwlp1=$nrgkickpwlp2
		evseip=$evseiplp2
		ipevseid=$evseidlp2
		chargep1ip=$chargep2ip
		chargep1cp=$chargep2cp
		twcmanagerlp1ip=$twcmanagerlp2ip
		twcmanagerlp1port=$twcmanagerlp2port
		twcmanagerlp1httpcontrol=$twcmanagerlp2httpcontrol
		owbpro1ip=$owbpro2ip
		# dirty call (no parameters, all is set above...)
		if (( lp2enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi

		setChargingCurrent

		echo $current > /var/www/html/openWB/ramdisk/llsolls1
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuss1
		if (( lp2enabled == 0 )); then
			current=$oldcurrent
		fi
	fi
fi

# set charging current - third charging point
if [[ $lastmanagements2 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "s2" ]]; then
		evsecon=$evsecons2
		dacregister=$dacregisters2
		modbusevsesource=$evsesources2
		modbusevseid=$evseids2
		evsewifitimeoutlp1=$evsewifitimeoutlp3
		evsewifiiplp1=$evsewifiiplp3
		goeiplp1=$goeiplp3
		goetimeoutlp1=$goetimeoutlp3
		evseip=$evseiplp3
		ipevseid=$evseidlp3
		chargep1ip=$chargep3ip
		chargep1cp=$chargep3cp
		owbpro1ip=$owbpro3ip
		if (( lp3enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolls2
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuss2
		if (( lp3enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
if [[ $lastmanagementlp4 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "lp4" ]]; then
		evsecon=$evseconlp4
		evseip=$evseiplp4
		ipevseid=$evseidlp4
		chargep1ip=$chargep4ip
		chargep1cp=$chargep4cp
		owbpro1ip=$owbpro4ip

		if (( lp4enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolllp4
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuslp4
		if (( lp4enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
if [[ $lastmanagementlp5 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "lp5" ]]; then
		evsecon=$evseconlp5
		evseip=$evseiplp5
		ipevseid=$evseidlp5
		chargep1ip=$chargep5ip
		chargep1cp=$chargep5cp
		owbpro1ip=$owbpro5ip

		if (( lp5enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolllp5
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuslp5
		if (( lp5enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
if [[ $lastmanagementlp6 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "lp6" ]]; then
		evsecon=$evseconlp6
		evseip=$evseiplp6
		ipevseid=$evseidlp6
		chargep1ip=$chargep6ip
		chargep1cp=$chargep6cp
		owbpro1ip=$owbpro6ip
		if (( lp6enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolllp6
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuslp6
		if (( lp6enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
if [[ $lastmanagementlp7 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "lp7" ]]; then
		evsecon=$evseconlp7
		evseip=$evseiplp7
		ipevseid=$evseidlp7
		chargep1ip=$chargep7ip
		chargep1cp=$chargep7cp
		owbpro1ip=$owbpro7ip

		if (( lp7enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolllp7
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuslp7
		if (( lp7enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
if [[ $lastmanagementlp8 == "1" ]]; then
	if [[ $points == "all" ]] || [[ $points == "lp8" ]]; then
		evsecon=$evseconlp8
		evseip=$evseiplp8
		ipevseid=$evseidlp8
		chargep1ip=$chargep8ip
		chargep1cp=$chargep8cp
		owbpro1ip=$owbpro8ip

		if (( lp8enabled == 0 )); then
			oldcurrent=$current
			current=0
		fi
		# dirty call (no parameters, all is set above...)
		setChargingCurrent
		echo $current > /var/www/html/openWB/ramdisk/llsolllp8
		echo $lstate > /var/www/html/openWB/ramdisk/ladestatuslp8
		if (( lp8enabled == 0 )); then
			current=$oldcurrent
		fi

	fi
fi
