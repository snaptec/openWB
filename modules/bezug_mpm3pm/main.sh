#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

if [[ "$mpm3pmevusource" = "*virtual*" ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$mpm3pmevusource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$mpm3pmevusource,raw tcp:$sdm630modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "bezug_mpm3pm.readmpm3pm" "${mpm3pmevusource}" "${mpm3pmevuid}" >>"${MYLOGFILE}" 2>&1
ret=$?
openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"

wattbezug=$(<"$RAMDISKDIR/wattbezug")
echo "$wattbezug"

if (( mpm3pmevuhaus == 1 )); then
	evua1=$(<"$RAMDISKDIR/bezuga1")
	evua2=$(<"$RAMDISKDIR/bezuga2")
	evua3=$(<"$RAMDISKDIR/bezuga3")
	lla1=$(<"$RAMDISKDIR/lla1")
	lla2=$(<"$RAMDISKDIR/lla2")
	lla3=$(<"$RAMDISKDIR/lla3")
	llas11=$(<"$RAMDISKDIR/llas11")
	llas12=$(<"$RAMDISKDIR/llas12")
	llas13=$(<"$RAMDISKDIR/llas13")
	bezuga1=$(echo "($evua1+$lla1+$llas12)" |bc)	
	bezuga2=$(echo "($evua2+$lla2+$llas13)" |bc)	
	bezuga3=$(echo "($evua3+$lla3+$llas11)" |bc)	
	echo "$bezuga1" > "$RAMDISKDIR/bezuga1"
	echo "$bezuga2" > "$RAMDISKDIR/bezuga2"
	echo "$bezuga3" > "$RAMDISKDIR/bezuga3"
fi
