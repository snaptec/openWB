#!/bin/bash

echo "Start cron nightly @ $(date)"

#logfile aufräumen
echo "$(tail -1000 /var/log/openWB.log)" > /var/log/openWB.log






monthlyfile="/var/www/html/openWB/web/logging/data/monthly/$(date +%Y%m)"

bezug=$(</var/www/html/openWB/ramdisk/bezugkwh)
einspeisung=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
pv=$(</var/www/html/openWB/ramdisk/pvkwh)
ll1=$(</var/www/html/openWB/ramdisk/llkwh)
ll2=$(</var/www/html/openWB/ramdisk/llkwhs1)
ll3=$(</var/www/html/openWB/ramdisk/llkwhs2)
llg=$(</var/www/html/openWB/ramdisk/llkwhges)
speicherikwh=$(</var/www/html/openWB/ramdisk/speicherikwh)
speicherekwh=$(</var/www/html/openWB/ramdisk/speicherekwh)




ll1=$(echo "$ll1 * 1000" | bc)
ll2=$(echo "$ll2 * 1000" | bc)
ll3=$(echo "$ll3 * 1000" | bc)
llg=$(echo "$llg * 1000" | bc)

echo $(date +%Y%m%d),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg >> $monthlyfile.csv
echo $(date +%Y%m%d) >> $monthlyfile-date.csv
echo $bezug >> $monthlyfile-bezug.csv
echo $einspeisung >> $monthlyfile-einspeisung.csv
echo $pv >> $monthlyfile-pv.csv
echo $ll1 >> $monthlyfile-ll1.csv
echo $ll2 >> $monthlyfile-ll2.csv
echo $ll3 >> $monthlyfile-ll3.csv
echo $llg >> $monthlyfile-llg.csv
echo $speicheri >> $monthlyfile-speicheriwh.csv
echo $speichere >> $monthlyfile-speicherewh.csv








