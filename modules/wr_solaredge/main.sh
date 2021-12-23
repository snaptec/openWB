#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

Solaredgebatwr="0"
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	Solaredgebatwr="1"  
fi
if [[ $solaredgewr2ip != "none" ]]; then
	python /var/www/html/openWB/modules/wr_solaredge/solaredge2wr.py $solaredgepvip $solaredgepvslave1 $Solaredgebatwr $solaredgewr2ip $wr1extprod
else
	python3 /var/www/html/openWB/modules/wr_solaredge/solaredgeall.py $solaredgepvip $solaredgepvslave1 $solaredgepvslave2 $solaredgepvslave3 $solaredgepvslave4 $Solaredgebatwr $wr1extprod $solaredgezweiterspeicher $solaredgesubbat >> "${RAMDISKDIR}/openWB.log" 2>&1
fi

cat /var/www/html/openWB/ramdisk/pvwatt
