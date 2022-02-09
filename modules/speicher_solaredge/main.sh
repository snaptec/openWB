#!/bin/bash
if [[ $solaredgespeicherip == $solaredgepvip ]]  ; then
	echo "value read at pv modul" > /dev/null
else
	OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
	python3 "$OPENWBBASEDIR/modules/speicher_solaredge/solaredge.py" "$solaredgespeicherip" "$solaredgezweiterspeicher" >> "${OPENWBBASEDIR}/ramdisk/openWB.log" 2>&1
fi
