#!/bin/bash

DMOD="MAIN"

python3 /var/www/html/openWB/modules/speicher_json/read_json.py "${battjsonurl}" "${battjsonwatt}" "${battjsonsoc}"

speicherleistung=$(</var/www/html/openWB/ramdisk/speicherleistung)
openwbDebugLog ${DMOD} 1 "BattLeistung: ${speicherleistung}"
echo ${speicherleistung}

battsoc=$(</var/www/html/openWB/ramdisk/speichersoc)
openwbDebugLog ${DMOD} 1 "BattSoC: ${battsoc}"
