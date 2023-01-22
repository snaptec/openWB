#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
Debug=$debug

pvwatt=0

# This script queries the microinverter Deye SUN600/800/1000G3-EU-230 device series for currently
# generated power values (for more details about this Deye microinverter series please have a look at
# https://deye.com/product/sun600-800-1000g3-eu-230-600-1000w-single-phase-2-mppt-micro-inverter-rapid-shutdown/)
#
# The Deye microinverters are also sold under the name Bosswerk. 
#
# This script is tested against this Deye SUN600G3-EU-230 device with firmware version:
#  * Firmware version: MW3_15U_5406_1.471 which consists of these components:
#  		* Communication Protocol Version：V0.2.0.1
#  		* Control Board Firmware Version：V0.1.1.4
#  		* Communication Board Firmware Version：V0.2.1.1
#
# This script is inspired by this great work: https://github.com/dr-ni/mi600

#For Development only
Debug=0

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

host=""
username=""
password=""

# credentials
if [ ${Debug} == 1 ]; then
	host="192.168.0.165"
	username="admin"
	password="Wvj3Bo4t4ZbLSt"
else
	host="${wr2deyehost}"
	username="${wr2deyeusername}"
	password="${wr2deyepassword}"
fi
auth=$username:$password

# get the current generated power value
dat="webdata_now_p"
val="W"

# ping host to check if the WR is online
ping -c3 $host > /dev/null 2>&1
if [ $? -eq 0 ]
then
	p=""
	retrycounter=0
	while [ $retrycounter -lt 5 ]
  	do
		p=$(curl -s -u "$auth" "$host"/status.html | grep "$dat = " | awk -F '"' '{print $2}')
  	
  		if [ $p != "" ]; then
  			break
  		fi
		((retrycounter++))
		if [ ${Debug} == 1 ]; then
  			echo "curl retry: $retrycounter"
  		fi
  		sleep 5
	done
  
  	if [ "$p" != "" ]
 	then
    	if [ ${Debug} == 1 ]; then
    		echo "$p $val"
    	fi
    	openwbDebugLog ${DMOD} 1 "${p} ${val}"
    	pvwatt="$p"
  	else
  		if [ ${Debug} == 1 ]; then
  			echo "0 $val"
  		fi
  		openwbDebugLog ${DMOD} 0 "Error: no power value provided by the microinverter -> set it to 0"
  		openwbDebugLog ${DMOD} 0 "0 ${val}"
  		pvwatt=0
  	fi
else
  	if [ ${Debug} == 1 ]; then
 		echo "Error: connection to $host failed"
  	fi
  	openwbDebugLog ${DMOD} 0 "Error: connection to $host failed"
  	pvwatt=0
fi

# following the instructions of https://github.com/snaptec/openWB#module-erstellen
echo "$pvwatt"
echo "$pvwatt" > "$RAMDISKDIR"/pvwatt

#bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.deye.device" "inverter" "$host" "pv2watt" >> "$MYLOGFILE" 2>&1
#ret=$?
#openwbDebugLog ${DMOD} 2 "RET: ${ret}"