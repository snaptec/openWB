#!/bin/bash
#daten holen und umformatieren
#python3 /var/www/html/openWB/runs/csvselmonth.py --input /var/www/html/openWB/web/logging/data/v001/ --output /var/www/html/openWB/ramdisk/ --partial /var/www/html/openWB/ramdisk/ --date $1 >> /var/www/html/openWB/ramdisk/csvselmonth.log 2>&1 &
echo "startet $1 "  >> /var/www/html/openWB/ramdisk/csvselmonth.log
python3 /var/www/html/openWB/runs/csvselmonth.py --input /var/www/html/openWB/web/logging/data/v001/ --output /var/www/html/openWB/ramdisk/ --partial /var/www/html/openWB/ramdisk/ --date $1 >> /var/www/html/openWB/ramdisk/csvselmonth.log 2>&1
# file 1 -> headerst
# file 2 -> Zaehler summe
# file 3 -> beträge summe
# file 4 -> Zaehler detail
# file 5 -> beträge detail

mosquitto_pub -t openWB/system/MonthGraphDatan1 -r -f /var/www/html/openWB/ramdisk/a_onl1 &
mosquitto_pub -t openWB/system/MonthGraphDatan2 -r -f /var/www/html/openWB/ramdisk/a_onl2 &
mosquitto_pub -t openWB/system/MonthGraphDatan3 -r -f /var/www/html/openWB/ramdisk/a_onl3 &
mosquitto_pub -t openWB/system/MonthGraphDatan4 -r -f /var/www/html/openWB/ramdisk/a_onl4 &
mosquitto_pub -t openWB/system/MonthGraphDatan5 -r -f /var/www/html/openWB/ramdisk/a_onl5 &
mosquitto_pub -t openWB/system/MonthGraphDatan6 -r -f /var/www/html/openWB/ramdisk/a_onl6 &
mosquitto_pub -t openWB/system/MonthGraphDatan7 -r -f /var/www/html/openWB/ramdisk/a_onl7 &
mosquitto_pub -t openWB/system/MonthGraphDatan8 -r -m "0" &
mosquitto_pub -t openWB/system/MonthGraphDatan9 -r -m "0" &
mosquitto_pub -t openWB/system/MonthGraphDatan10 -r -m "0" &
mosquitto_pub -t openWB/system/MonthGraphDatan11 -r -m "0" &
mosquitto_pub -t openWB/system/MonthGraphDatan12 -r -m "0" &

(sleep 1 && mosquitto_pub -t openWB/set/graph/RequestMonthGraphv1 -r -m "0")&
