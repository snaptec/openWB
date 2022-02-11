#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname $0)"/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "wr_fronius: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

openwbDebugLog ${DMOD} 2 "WR IP: ${wrfroniusip}"
openwbDebugLog ${DMOD} 2 "WR IP2: ${wrfronius2ip}"
openwbDebugLog ${DMOD} 2 "WR Speicher: ${speichermodul}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.fronius.device" "inverter" "${wrfroniusip}" "0" "0" "0" "${wrfronius2ip}" "${speichermodul}" "1" 2>>$MYLOGFILE

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
