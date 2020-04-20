#!/bin/bash
. /var/www/html/openWB/openwb.conf
dailyfile="/var/www/html/openWB/web/logging/data/daily/$(date +%Y%m%d)"
monthlyladelogfile="/var/www/html/openWB/web/logging/data/ladelog/$(date +%Y%m).csv"

linesladelog=$(cat $monthlyladelogfile | wc -l)
if [[ "$linesladelog" == 0 ]]; then
	echo > $monthlyladelogfile
fi
bezug=$(</var/www/html/openWB/ramdisk/bezugkwh)
einspeisung=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
if [[ $pv2wattmodul != "none" ]]; then
	pv=$(</var/www/html/openWB/ramdisk/pvallwh)
else
	pv=$(</var/www/html/openWB/ramdisk/pvkwh)
fi
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
verbraucher1=$(</var/www/html/openWB/ramdisk/verbraucher1_wh)
verbraucher2=$(</var/www/html/openWB/ramdisk/verbraucher2_wh)
verbraucher3=$(</var/www/html/openWB/ramdisk/verbraucher3_wh)
verbrauchere1=$(</var/www/html/openWB/ramdisk/verbraucher1_whe)
verbrauchere2=$(</var/www/html/openWB/ramdisk/verbraucher2_whe)
ll4=$(</var/www/html/openWB/ramdisk/llkwhlp4)
ll5=$(</var/www/html/openWB/ramdisk/llkwhlp5)
ll6=$(</var/www/html/openWB/ramdisk/llkwhlp6)
ll7=$(</var/www/html/openWB/ramdisk/llkwhlp7)
ll8=$(</var/www/html/openWB/ramdisk/llkwhlp8)
ll4=$(echo "$ll4 * 1000" | bc)
ll5=$(echo "$ll5 * 1000" | bc)
ll6=$(echo "$ll6 * 1000" | bc)
ll7=$(echo "$ll7 * 1000" | bc)
ll8=$(echo "$ll8 * 1000" | bc)
temp1=$(</var/www/html/openWB/ramdisk/device1_temp0)
temp2=$(</var/www/html/openWB/ramdisk/device1_temp1)
temp3=$(</var/www/html/openWB/ramdisk/device1_temp2)
temp4=$(</var/www/html/openWB/ramdisk/device2_temp0)
temp5=$(</var/www/html/openWB/ramdisk/device2_temp1)
temp6=$(</var/www/html/openWB/ramdisk/device2_temp2)
d1=$(</var/www/html/openWB/ramdisk/device1_wh)
d2=$(</var/www/html/openWB/ramdisk/device2_wh)
d3=$(</var/www/html/openWB/ramdisk/device3_wh)
d4=$(</var/www/html/openWB/ramdisk/device4_wh)
d5=$(</var/www/html/openWB/ramdisk/device5_wh)
d6=$(</var/www/html/openWB/ramdisk/device6_wh)
d7=$(</var/www/html/openWB/ramdisk/device7_wh)
d8=$(</var/www/html/openWB/ramdisk/device8_wh)
d9=$(</var/www/html/openWB/ramdisk/device9_wh)
d10=$(</var/www/html/openWB/ramdisk/device10_wh)



echo $(date +%H%M),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg,$speicheri,$speichere,$verbraucher1,$verbrauchere1,$verbraucher2,$verbrauchere2,$verbraucher3,$ll4,$ll5,$ll6,$ll7,$ll8,$speichersoc,$soc,$soc1,$temp1,$temp2,$temp3,$d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9,$d10,$temp4,$temp5,$temp6 >> $dailyfile.csv

netzabschaltunghz=0
if (( netzabschaltunghz == 1 )); then
hz=$(</var/www/html/openWB/ramdisk/llhz)
hz=$(echo "$hz * 100" | bc | sed 's/\..*$//')
netzschutz=$(</var/www/html/openWB/ramdisk/netzschutz)
	if (( netzschutz == 0 )); then
		if (( hz > 4500 )) && (( $hz < 5300 )); then
			if (( $hz > 5180 )); then
				lademodus=$(</var/www/html/openWB/ramdisk/lademodus)
				echo $lademodus > /var/www/html/openWB/ramdisk/templademodus
				echo 3 > /var/www/html/openWB/ramdisk/lademodus
				echo 1 > /var/www/html/openWB/ramdisk/netzschutz
			fi
			if (( hz < 4920 )); then
				lademodus=$(</var/www/html/openWB/ramdisk/lademodus)
				echo $lademodus > /var/www/html/openWB/ramdisk/templademodus
				echo 1 > /var/www/html/openWB/ramdisk/netzschutz
				(sleep $(shuf -i1-90 -n1) && echo 3 > /var/www/html/openWB/ramdisk/lademodus) &
			fi

		fi
	else
		if (( hz > 4500 )) && (( $hz < 5300 )); then
			if (( $hz < 5100 )); then
				templademodus=$(</var/www/html/openWB/ramdisk/templademodus)
				echo $templademodus > /var/www/html/openWB/ramdisk/lademodus
				echo 0 > /var/www/html/openWB/ramdisk/netzschutz
			fi
			if (( $hz > 4960 )); then
				templademodus=$(</var/www/html/openWB/ramdisk/templademodus)
				echo $templademodus > /var/www/html/openWB/ramdisk/lademodus
				echo 0 > /var/www/html/openWB/ramdisk/netzschutz
			fi
		fi
	fi
fi
if (( awattaraktiv == 1 )); then
	/var/www/html/openWB/runs/awattargetprices.sh
fi
pvkwh=$(</var/www/html/openWB/ramdisk/pvkwh)

pvdailyyieldstart=$(head -n 1 /var/www/html/openWB/web/logging/data/daily/$(date +%Y%m%d).csv)
pvyieldcount=0
for i in ${pvdailyyieldstart//,/ }
do
	pvyieldcount=$((pvyieldcount + 1 ))
	if (( pvyieldcount == 4 )); then

		pvdailyyield=$(echo "scale=2;($pvkwh - $i) / 1000" |bc)
		echo $pvdailyyield > /var/www/html/openWB/ramdisk/daily_pvkwhk
	fi
done
ip route get 1 | awk '{print $NF;exit}' > /var/www/html/openWB/ramdisk/ipaddress


echo "$(tail -1000 /var/www/html/openWB/ramdisk/smarthome.log)" > /var/www/html/openWB/ramdisk/smarthome.log
echo "$(tail -1000 /var/www/html/openWB/ramdisk/mqtt.log)" > /var/www/html/openWB/ramdisk/mqtt.log

if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/mqttsub.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 /var/www/html/openWB/runs/mqttsub.py &
fi
if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/smarthomehandler.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 /var/www/html/openWB/runs/smarthomehandler.py &
fi

