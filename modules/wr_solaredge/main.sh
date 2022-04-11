#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

Solaredgebatwr="0"
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	Solaredgebatwr="1"  
fi
if [[ $solaredgewr2ip != "none" ]]; then
	python /var/www/html/openWB/modules/wr_solaredge/solaredge2wr.py $solaredgepvip $solaredgepvslave1 $Solaredgebatwr $solaredgewr2ip $wr1extprod
else
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_solaredge.solaredgeall" $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $solaredgepvslave3 $solaredgepvslave4 $Solaredgebatwr $wr1extprod $solaredgezweiterspeicher $solaredgesubbat >>$MYLOGFILE 2>&1
	ret=$?
	openwbDebugLog ${DMOD} 2 "RET: ${ret}"
fi

watt=$(<${RAMDISKDIR}/pvwatt)
echo ${watt}
