#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="MAIN"

openwbDebugLog ${DMOD} 2 "RCT Bezug start"

wattbezug=$(echo "scale=0; $(python "${MODULEDIR}/rct_read.py" --ip="$bezug1_ip" --name='g_sync.p_ac_sc_sum')/1" | bc)
openwbDebugLog ${DMOD} 2 "Bezug RCT Leistung: ${wattbezug}"

watt1=$(echo "scale=0; $(python "${MODULEDIR}/rct_read.py" --ip="$bezug1_ip" --id='0x27BE51D9')/230/1" | bc)
watt2=$(echo "scale=0; $(python "${MODULEDIR}/rct_read.py" --ip="$bezug1_ip" --id='0xF5584F90')/230/1" | bc)
watt3=$(echo "scale=0; $(python "${MODULEDIR}/rct_read.py" --ip="$bezug1_ip" --id='0xB221BCFA')/230/1" | bc)
openwbDebugLog ${DMOD} 2 "Bezug RCT Strom L1: ${watt1} L2: ${watt2} L3: ${watt3}"

echo "$watt1" > "${RAMDISKDIR}/bezuga1"
echo "$watt2" > "${RAMDISKDIR}/bezuga2"
echo "$watt3" > "${RAMDISKDIR}/bezuga3"
echo "$wattbezug" > "${RAMDISKDIR}/wattbezug"

# Gebe wattbezug als Ergbenis mit zurueck da beim Bezug-Module ein Returnwert erwartet wird.
echo "$wattbezug"
