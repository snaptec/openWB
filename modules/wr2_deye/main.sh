#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
Debug=$debug

# This script queries the microinverter Deye SUN600/800/1000G3-EU-230 device series for currently
# generated power values (for more details about this Deye microinverter series please have a look at
# https://deye.com/product/sun600-800-1000g3-eu-230-600-1000w-single-phase-2-mppt-micro-inverter-rapid-shutdown/)
#
# The Deye microinverters are also sold under the same Bosswerk. 
#
# This script is tested against this Deye SUN600G3-EU-230 device with firmware version:
#  * Communication Protocol Version：V0.2.0.1
#  * Control Board Firmware Version：V0.1.1.4
#  * Communication Board Firmware Version：V0.2.1.1
#
# This script is inspired by this great work: https://github.com/dr-ni/mi600

#For Development only
Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

#openwbDebugLog ${DMOD} 2 "PV URL : ${wr2jsonurl}"
#openwbDebugLog ${DMOD} 2 "PV Watt: ${wr2jsonwatt}"
#openwbDebugLog ${DMOD} 2 "PV kWh : ${wr2jsonkwh}"

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
  p=$(curl -s -u "$auth" "$host"/status.html | grep "$dat = " | awk -F '"' '{print $2}')
  if [ "$p" = "" ]
  then
    sleep 3
    p=$(curl -s -u "$auth" "$host"/status.html | grep "$dat = " | awk -F '"' '{print $2}')
  fi
  if [ "$p" = "" ]
  then
    sleep 3
    p=$(curl -s -u "$auth" "$host"/status.html | grep "$dat = " | awk -F '"' '{print $2}')
  fi
  if [ "$p" = "" ]
  then
    sleep 3
    p=$(curl -s -u "$auth" "$host"/status.html | grep "$dat = " | awk -F '"' '{print $2}')
  fi
  if [ "$p" != "" ]
  then
    echo "$p $val"
    openwbDebugLog ${DMOD} 2 "${p} ${val}"
    exit 0
  fi
  echo "Error: could not read $4"
  openwbDebugLog ${DMOD} 2 "Error: could not read $4"
  exit 1
else
  echo "Error: connection to $host failed"
  openwbDebugLog ${DMOD} 2 "Error: connection to $host failed"
  exit 1
fi


#bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.json.device" "inverter" "${wr2deyehost}" "${wr2jsonwatt}" "${wr2jsonkwh}" "2" >>"$MYLOGFILE" 2>&1
#ret=$?

#openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/pv2watt"