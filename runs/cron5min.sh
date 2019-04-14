#!/bin/bash

dailyfile="/var/www/html/openWB/web/logging/data/daily/$(date +%Y%m%d)"

bezug=$(</var/www/html/openWB/ramdisk/bezugkwh)
einspeisung=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
pv=$(</var/www/html/openWB/ramdisk/pvkwh)
ll1=$(</var/www/html/openWB/ramdisk/llkwh)
ll2=$(</var/www/html/openWB/ramdisk/llkwhs1)
ll3=$(</var/www/html/openWB/ramdisk/llkwhs2)
llg=$(</var/www/html/openWB/ramdisk/llkwhges)
soc=$(</var/www/html/openWB/ramdisk/soc)
soc1=$(</var/www/html/openWB/ramdisk/soc1)
speicheri=$(</var/www/html/openWB/ramdisk/speicherikwh)
speichere=$(</var/www/html/openWB/ramdisk/speicherekwh)
speichersoc=$(</var/www/html/openWB/ramdisk/speichersoc)
ll1=$(echo "$ll1 * 1000" | bc)
ll2=$(echo "$ll2 * 1000" | bc)
ll3=$(echo "$ll3 * 1000" | bc)
llg=$(echo "$llg * 1000" | bc)

echo $(date +%H%M),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg,$speicheri,$speichere >> $dailyfile.csv
echo $(date +%H%M) >> $dailyfile-date.csv
echo $bezug >> $dailyfile-bezug.csv
echo $einspeisung >> $dailyfile-einspeisung.csv
echo $pv >> $dailyfile-pv.csv
echo $ll1 >> $dailyfile-ll1.csv
echo $ll2 >> $dailyfile-ll2.csv
echo $ll3 >> $dailyfile-ll3.csv
echo $llg >> $dailyfile-llg.csv
echo $soc >> $dailyfile-soc.csv
echo $speicheri >> $dailyfile-speicheriwh.csv
echo $speichere >> $dailyfile-speicherewh.csv
echo $soc1 >> $dailyfile-soc1.csv
echo $speichersoc >> $dailyfile-speichersoc.csv







