#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
#DMOD="BAT"
DMOD="MAIN"
Debug=$debug

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
        MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
        MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

# Auslesen eines Varta Speicher über die integrierte XML-API der Batteroe.

if [[ "$usevartamodbus" != "1" ]]; then
	speicherwatt=$(curl --connect-timeout 3 -s "$vartaspeicherip/cgi/ems_data.xml" | grep 'P' | sed 's/.*value=//' |tr -d "'/>")
	# wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
	ra='^-?[0-9]+$'
	if [[ $speicherwatt =~ $ra ]] ; then
		echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung
	fi
	speichersoc=$(curl --connect-timeout 3 -s "$vartaspeicherip/cgi/ems_data.xml" | grep 'SOC' | sed 's/.*value=//' |tr -d "'/>")
	# if [[ $speichersoc -ge "101" ]]; then
	speichersoc=$(echo "$speichersoc / 10" |bc)
	# fi
	if [[ $speichersoc =~ $ra ]] ; then
		echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc
	fi
else 
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "speicher_varta.varta" "${vartaspeicherip}" "${vartaspeicher2ip}" >>${MYLOGFILE} 2>&1
	ret=$?
	openwbDebugLog ${DMOD} 2 "RET: ${ret}"
fi
