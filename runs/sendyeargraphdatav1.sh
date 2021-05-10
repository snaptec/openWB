#!/bin/bash

echo "startet $1 "  >> /var/www/html/openWB/ramdisk/csvselyear.log
python3 /var/www/html/openWB/runs/csvselyear.py --input /var/www/html/openWB/web/logging/data/v001/ --output /var/www/html/openWB/ramdisk/ --partial /var/www/html/openWB/ramdisk/ --date $1 >> /var/www/html/openWB/ramdisk/csvselyear.log 2>&1

mosquitto_pub -t openWB/system/YearGraphDatan1 -r -r -f /var/www/html/openWB/ramdisk/b_onl1 &
mosquitto_pub -t openWB/system/YearGraphDatan2 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan3 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan4 -r -f /var/www/html/openWB/ramdisk/b_onl4 &
mosquitto_pub -t openWB/system/YearGraphDatan5 -r -f /var/www/html/openWB/ramdisk/b_onl5 &
mosquitto_pub -t openWB/system/YearGraphDatan6 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan7 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan8 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan9 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan10 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan11 -r -m  "0" &
mosquitto_pub -t openWB/system/YearGraphDatan12 -r -m  "0" &

(sleep 1 && mosquitto_pub -t openWB/set/graph/RequestYearGraphv1 -r -m "0") &
