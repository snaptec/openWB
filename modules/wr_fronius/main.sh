#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
        MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
        MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

openwbDebugLog ${DMOD} 2 "WR IP: ${wrfroniusip}"
openwbDebugLog ${DMOD} 2 "WR Gen 24: ${wrfroniusisgen24}"
openwbDebugLog ${DMOD} 2 "WR IP2: ${wrfronius2ip}"

python3 /var/www/html/openWB/packages/modules/fronius/device.py "inverter" "${wrfroniusip}" "0" "${wrfroniusisgen24}" "0" "0" "0" "${wrfronius2ip}" "${speichermodul}" "1" &>>$MYLOGFILE
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
