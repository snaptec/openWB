#!/bin/bash
. /var/www/html/openWB/loadconfig.sh
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
pvkwh=$pv

pvdailyyieldstart=$(head -n 1 /var/www/html/openWB/web/logging/data/daily/$(date +%Y%m%d).csv)
pvyieldcount=0
for i in ${pvdailyyieldstart//,/ }
do
	pvyieldcount=$((pvyieldcount + 1 ))
	if (( pvyieldcount == 2 )); then
		bezugdailyyield=$(echo "scale=2;($bezug - $i) / 1000" |bc)
		echo $bezugdailyyield > /var/www/html/openWB/ramdisk/daily_bezugkwh
	fi

	if (( pvyieldcount == 3 )); then
		einspeisungdailyyield=$(echo "scale=2;($einspeisung - $i) / 1000" |bc)
		echo $einspeisungdailyyield > /var/www/html/openWB/ramdisk/daily_einspeisungkwh
	fi
	if (( pvyieldcount == 4 )); then
		pvdailyyield=$(echo "scale=2;($pvkwh - $i) / 1000" |bc)
		echo $pvdailyyield > /var/www/html/openWB/ramdisk/daily_pvkwhk
	fi
	if (( pvyieldcount == 8 )); then
		lladailyyield=$(echo "scale=2;($llg - $i) / 1000" |bc)
		echo $lladailyyield > /var/www/html/openWB/ramdisk/daily_llakwh
	fi
	if (( pvyieldcount == 9 )); then
		sidailyyield=$(echo "scale=2;($speicheri - $i) / 1000" |bc)
		echo $sidailyyield > /var/www/html/openWB/ramdisk/daily_sikwh
	fi
	if (( pvyieldcount == 10 )); then
		sedailyyield=$(echo "scale=2;($speichere - $i) / 1000" |bc)
		echo $sedailyyield > /var/www/html/openWB/ramdisk/daily_sekwh
	fi
	if (( pvyieldcount == 27 )); then
		d1dailyyield=$(echo "scale=2;($d1 - $i) / 1000" |bc)
		echo $d1dailyyield > /var/www/html/openWB/ramdisk/daily_d1kwh
	fi
	if (( pvyieldcount == 28 )); then
		d2dailyyield=$(echo "scale=2;($d2 - $i) / 1000" |bc)
		echo $d2dailyyield > /var/www/html/openWB/ramdisk/daily_d2kwh
	fi
	if (( pvyieldcount == 29 )); then
		d3dailyyield=$(echo "scale=2;($d3 - $i) / 1000" |bc)
		echo $d3dailyyield > /var/www/html/openWB/ramdisk/daily_d3kwh
	fi
	if (( pvyieldcount == 30 )); then
		d4dailyyield=$(echo "scale=2;($d4 - $i) / 1000" |bc)
		echo $d4dailyyield > /var/www/html/openWB/ramdisk/daily_d4kwh
	fi
	if (( pvyieldcount == 31 )); then
		d5dailyyield=$(echo "scale=2;($d5 - $i) / 1000" |bc)
		echo $d5dailyyield > /var/www/html/openWB/ramdisk/daily_d5kwh
	fi

done
hausdailyyield=$(echo "scale=2;$bezugdailyyield + $pvdailyyield - $lladailyyield + $sedailyyield - $sidailyyield - $einspeisungdailyyield - $d1dailyyield - $d2dailyyield - $d3dailyyield - $d4dailyyield - $d5dailyyield" | bc)
echo $hausdailyyield > /var/www/html/openWB/ramdisk/daily_hausverbrauchkwh

ip route get 1 | awk '{print $NF;exit}' > /var/www/html/openWB/ramdisk/ipaddress


echo "$(tail -500 /var/www/html/openWB/ramdisk/smarthome.log)" > /var/www/html/openWB/ramdisk/smarthome.log
echo "$(tail -500 /var/www/html/openWB/ramdisk/mqtt.log)" > /var/www/html/openWB/ramdisk/mqtt.log
echo "$(tail -500 /var/www/html/openWB/ramdisk/nurpv.log)" > /var/www/html/openWB/ramdisk/nurpv.log


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

if (( isss == 1 )); then
       if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/isss.py" > /dev/null
       then
               echo "test" > /dev/null
       else
               python3 /var/www/html/openWB/runs/isss.py &
       fi
else
	ethstate=$(</sys/class/net/eth0/carrier)
	if (( ethstate == 1 )); then
		sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
		sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 down

	else
		sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up
		sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 down

	fi
fi
if [[ "$evsecon" == "buchse" ]]; then
       if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/buchse.py" > /dev/null
       then
               echo "test" > /dev/null
       else
               python3 /var/www/html/openWB/runs/buchse.py &
       fi
fi
if [[ "$rfidakt" == "2" ]]; then
	echo $rfidlist > /var/www/html/openWB/ramdisk/rfidlist
       if ps ax |grep -v grep |grep "python3 /var/www/html/openWB/runs/rfid.py" > /dev/null
       then
               echo "test" > /dev/null
       else
               python3 /var/www/html/openWB/runs/rfid.py &
       fi
fi
