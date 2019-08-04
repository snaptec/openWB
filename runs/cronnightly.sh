#!/bin/bash
. /var/www/html/openWB/openwb.conf
echo "Start cron nightly @ $(date)"
#gsi daten abfragen
/var/www/html/openWB/runs/gsiabfrage.sh &
#logfile aufräumen
echo "$(tail -1000 /var/log/openWB.log)" > /var/log/openWB.log
echo 1 > /var/www/html/openWB/ramdisk/reloaddisplay






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
verbraucher1iwh=$(</var/www/html/openWB/ramdisk/verbraucher1_wh)
verbraucher1ewh=$(</var/www/html/openWB/ramdisk/verbraucher1_whe)
verbraucher2iwh=$(</var/www/html/openWB/ramdisk/verbraucher2_wh)
verbraucher2ewh=$(</var/www/html/openWB/ramdisk/verbraucher2_whe)






ll1=$(echo "$ll1 * 1000" | bc)
ll2=$(echo "$ll2 * 1000" | bc)
ll3=$(echo "$ll3 * 1000" | bc)
llg=$(echo "$llg * 1000" | bc)

echo $(date +%Y%m%d),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg,$verbraucher1iwh,$verbraucher1ewh,$verbraucher2iwh,$verbraucher2ewh >> $monthlyfile.csv
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
echo $verbraucher1iwh >> $monthlyfile-verbraucher1iwh.csv
echo $verbraucher1ewh >> $monthlyfile-verbraucher1ewh.csv
echo $verbraucher2iwh >> $monthlyfile-verbraucher2iwh.csv
echo $verbraucher2ewh >> $monthlyfile-verbraucher2ewh.csv


if [[ $verbraucher1_typ == "tasmota" ]]; then
	verbraucher1_oldwh=$(curl -s http://$verbraucher1_ip/cm?cmnd=Status%208 | jq '.StatusSNS.ENERGY.Total')
	if [[ $? == "0" ]]; then
		verbraucher1_writewh=$(echo "scale=0;(($verbraucher1_oldwh * 1000) + $verbraucher1_tempwh) / 1" | bc)
		sed -i "s/verbraucher1_tempwh=.*/verbraucher1_tempwh=$verbraucher1_writewh/" /var/www/html/openWB/openwb.conf
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset1%200
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset2%200
		curl -s http://$verbraucher1_ip/cm?cmnd=EnergyReset3%200
	fi
fi
if [[ $verbraucher2_typ == "tasmota" ]]; then
	verbraucher2_oldwh=$(curl -s http://$verbraucher2_ip/cm?cmnd=Status%208 | jq '.StatusSNS.ENERGY.Total')
	if [[ $? == "0" ]]; then
		verbraucher2_writewh=$(echo "scale=0;(($verbraucher2_oldwh * 1000) + $verbraucher2_tempwh) / 1" | bc)
		sed -i "s/verbraucher2_tempwh=.*/verbraucher2_tempwh=$verbraucher2_writewh/" /var/www/html/openWB/openwb.conf
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset1%200
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset2%200
		curl -s http://$verbraucher2_ip/cm?cmnd=EnergyReset3%200
	fi
fi


