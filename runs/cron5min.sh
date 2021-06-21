#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"

. $OPENWBBASEDIR/loadconfig.sh

dailyfile="$OPENWBBASEDIR/web/logging/data/daily/$(date +%Y%m%d)"
monthlyladelogfile="$OPENWBBASEDIR/web/logging/data/ladelog/$(date +%Y%m).csv"

# check if a monthly logfile exists and create a new one if not
linesladelog=$(cat $monthlyladelogfile | wc -l)
if [[ "$linesladelog" == 0 ]]; then
	echo > $monthlyladelogfile
fi

# calculate daily stats
bezug=$(<$RAMDISKDIR/bezugkwh)
einspeisung=$(<$RAMDISKDIR/einspeisungkwh)
if [[ $pv2wattmodul != "none" ]]; then
	pv=$(<$RAMDISKDIR/pvallwh)
else
	pv=$(<$RAMDISKDIR/pvkwh)
fi
ll1=$(<$RAMDISKDIR/llkwh)
ll2=$(<$RAMDISKDIR/llkwhs1)
ll3=$(<$RAMDISKDIR/llkwhs2)
llg=$(<$RAMDISKDIR/llkwhges)
soc=$(<$RAMDISKDIR/soc)
soc1=$(<$RAMDISKDIR/soc1)
speicheri=$(<$RAMDISKDIR/speicherikwh)
speichere=$(<$RAMDISKDIR/speicherekwh)
speichersoc=$(<$RAMDISKDIR/speichersoc)
ll1=$(echo "$ll1 * 1000" | bc)
ll2=$(echo "$ll2 * 1000" | bc)
ll3=$(echo "$ll3 * 1000" | bc)
llg=$(echo "$llg * 1000" | bc)
verbraucher1=$(<$RAMDISKDIR/verbraucher1_wh)
verbraucher2=$(<$RAMDISKDIR/verbraucher2_wh)
verbraucher3=$(<$RAMDISKDIR/verbraucher3_wh)
verbrauchere1=$(<$RAMDISKDIR/verbraucher1_whe)
verbrauchere2=$(<$RAMDISKDIR/verbraucher2_whe)
ll4=$(<$RAMDISKDIR/llkwhlp4)
ll5=$(<$RAMDISKDIR/llkwhlp5)
ll6=$(<$RAMDISKDIR/llkwhlp6)
ll7=$(<$RAMDISKDIR/llkwhlp7)
ll8=$(<$RAMDISKDIR/llkwhlp8)
ll4=$(echo "$ll4 * 1000" | bc)
ll5=$(echo "$ll5 * 1000" | bc)
ll6=$(echo "$ll6 * 1000" | bc)
ll7=$(echo "$ll7 * 1000" | bc)
ll8=$(echo "$ll8 * 1000" | bc)
temp1=$(<$RAMDISKDIR/device1_temp0)
temp2=$(<$RAMDISKDIR/device1_temp1)
temp3=$(<$RAMDISKDIR/device1_temp2)
temp4=$(<$RAMDISKDIR/device2_temp0)
temp5=$(<$RAMDISKDIR/device2_temp1)
temp6=$(<$RAMDISKDIR/device2_temp2)
d1=$(<$RAMDISKDIR/device1_wh)
d2=$(<$RAMDISKDIR/device2_wh)
d3=$(<$RAMDISKDIR/device3_wh)
d4=$(<$RAMDISKDIR/device4_wh)
d5=$(<$RAMDISKDIR/device5_wh)
d6=$(<$RAMDISKDIR/device6_wh)
d7=$(<$RAMDISKDIR/device7_wh)
d8=$(<$RAMDISKDIR/device8_wh)
d9=$(<$RAMDISKDIR/device9_wh)
d10="0"
# now add a line to our daily csv
echo $(date +%H%M),$bezug,$einspeisung,$pv,$ll1,$ll2,$ll3,$llg,$speicheri,$speichere,$verbraucher1,$verbrauchere1,$verbraucher2,$verbrauchere2,$verbraucher3,$ll4,$ll5,$ll6,$ll7,$ll8,$speichersoc,$soc,$soc1,$temp1,$temp2,$temp3,$d1,$d2,$d3,$d4,$d5,$d6,$d7,$d8,$d9,$d10,$temp4,$temp5,$temp6 >> $dailyfile.csv

# grid protection
# temporary disabled
# netzabschaltunghz=0
if (( netzabschaltunghz == 1 )); then
	hz=$(<$RAMDISKDIR/llhz)
	hz=$(echo "$hz * 100" | bc | sed 's/\..*$//')
	netzschutz=$(<$RAMDISKDIR/netzschutz)
	if (( netzschutz == 0 )); then
		# grid protection is not set
		if (( hz > 4500 )) && (( hz < 5300 )); then
			if (( hz > 5180 )); then
				# grid power overload detected
				# store current charge mode
				lademodus=$(<$RAMDISKDIR/lademodus)
				echo $lademodus > $RAMDISKDIR/templademodus
				# set charge mode to stop
				echo 3 > $RAMDISKDIR/lademodus
				# set grid protection
				echo 1 > $RAMDISKDIR/netzschutz
				echo "!!! Netzschutz aktiv !!!" > $RAMDISKDIR/lastregelungaktiv
			fi
			if (( hz < 4920 )); then
				# grid power underload detected
				# store current charge mode
				lademodus=$(<$RAMDISKDIR/lademodus)
				echo $lademodus > $RAMDISKDIR/templademodus
				# set grid protection
				echo 1 > $RAMDISKDIR/netzschutz
				echo "!!! Netzschutz aktiv !!!" > $RAMDISKDIR/lastregelungaktiv
				# wait a random interval and set charge mode to stop
				(sleep $(shuf -i1-90 -n1) && echo 3 > $RAMDISKDIR/lademodus) &
			fi
		fi
	else
		# grid protection is set
		if (( hz > 4960 )) && (( hz < 5100 )); then
			# grid is in normal load range
			# restore last charge mode
			templademodus=$(<$RAMDISKDIR/templademodus)
			echo $templademodus > $RAMDISKDIR/lademodus
			# remove grid protection
			echo 0 > $RAMDISKDIR/netzschutz
			echo "Netzfrequenz wieder im normalen Bereich." > $RAMDISKDIR/lastregelungaktiv
		fi
	fi
fi

# update electricity provider prices
if (( etprovideraktiv == 1 )); then
	$OPENWBBASEDIR/modules/$etprovider/main.sh &
fi

# update all daily yield stats
pvkwh=$pv
pvdailyyieldstart=$(head -n 1 $OPENWBBASEDIR/web/logging/data/daily/$(date +%Y%m%d).csv)
pvyieldcount=0
for i in ${pvdailyyieldstart//,/ }
do
	# pv
	pvyieldcount=$((pvyieldcount + 1 ))
	if (( pvyieldcount == 2 )); then
		bezugdailyyield=$(echo "scale=2;($bezug - $i) / 1000" |bc)
		echo $bezugdailyyield > $RAMDISKDIR/daily_bezugkwh
	fi
	if (( pvyieldcount == 3 )); then
		einspeisungdailyyield=$(echo "scale=2;($einspeisung - $i) / 1000" |bc)
		echo $einspeisungdailyyield > $RAMDISKDIR/daily_einspeisungkwh
	fi
	if (( pvyieldcount == 4 )); then
		pvdailyyield=$(echo "scale=2;($pvkwh - $i) / 1000" |bc)
		echo $pvdailyyield > $RAMDISKDIR/daily_pvkwhk
	fi
	# all charge points
	if (( pvyieldcount == 8 )); then
		lladailyyield=$(echo "scale=2;($llg - $i) / 1000" |bc)
		echo $lladailyyield > $RAMDISKDIR/daily_llakwh
	fi
	# house battery
	if (( pvyieldcount == 9 )); then
		sidailyyield=$(echo "scale=2;($speicheri - $i) / 1000" |bc)
		echo $sidailyyield > $RAMDISKDIR/daily_sikwh
	fi
	if (( pvyieldcount == 10 )); then
		sedailyyield=$(echo "scale=2;($speichere - $i) / 1000" |bc)
		echo $sedailyyield > $RAMDISKDIR/daily_sekwh
	fi
	# old smarthome devices
	if (( pvyieldcount == 11 )); then
		verbraucher1dailyyield=$(echo "scale=2;($verbraucher1 - $i) / 1000" |bc)
		echo $verbraucher1dailyyield > $RAMDISKDIR/daily_verbraucher1ikwh
	fi
	if (( pvyieldcount == 12 )); then
		verbrauchere1dailyyield=$(echo "scale=2;($verbrauchere1 - $i) / 1000" |bc)
		echo $verbrauchere1dailyyield > $RAMDISKDIR/daily_verbraucher1ekwh
	fi
	if (( pvyieldcount == 13 )); then
		verbraucher2dailyyield=$(echo "scale=2;($verbraucher2 - $i) / 1000" |bc)
		echo $verbraucher2dailyyield > $RAMDISKDIR/daily_verbraucher2ikwh
	fi
	if (( pvyieldcount == 14 )); then
		verbrauchere2dailyyield=$(echo "scale=2;($verbrauchere2 - $i) / 1000" |bc)
		echo $verbrauchere2dailyyield > $RAMDISKDIR/daily_verbraucher2ekwh
	fi
	if (( pvyieldcount == 15 )); then
		verbraucher3dailyyield=$(echo "scale=2;($verbraucher3 - $i) / 1000" |bc)
		echo $verbraucher3dailyyield > $RAMDISKDIR/daily_verbraucher3ikwh
	fi
	# smarthome 2.0 devices
	if (( pvyieldcount == 27 )); then
		d1dailyyield=$(echo "scale=2;($d1 - $i) / 1000" |bc)
		echo $d1dailyyield > $RAMDISKDIR/daily_d1kwh
	fi
	if (( pvyieldcount == 28 )); then
		d2dailyyield=$(echo "scale=2;($d2 - $i) / 1000" |bc)
		echo $d2dailyyield > $RAMDISKDIR/daily_d2kwh
	fi
	if (( pvyieldcount == 29 )); then
		d3dailyyield=$(echo "scale=2;($d3 - $i) / 1000" |bc)
		echo $d3dailyyield > $RAMDISKDIR/daily_d3kwh
	fi
	if (( pvyieldcount == 30 )); then
		d4dailyyield=$(echo "scale=2;($d4 - $i) / 1000" |bc)
		echo $d4dailyyield > $RAMDISKDIR/daily_d4kwh
	fi
	if (( pvyieldcount == 31 )); then
		d5dailyyield=$(echo "scale=2;($d5 - $i) / 1000" |bc)
		echo $d5dailyyield > $RAMDISKDIR/daily_d5kwh
	fi
	if (( pvyieldcount == 32 )); then
		d6dailyyield=$(echo "scale=2;($d6 - $i) / 1000" |bc)
		echo $d6dailyyield > $RAMDISKDIR/daily_d6kwh
	fi
	if (( pvyieldcount == 33 )); then
		d7dailyyield=$(echo "scale=2;($d7 - $i) / 1000" |bc)
		echo $d7dailyyield > $RAMDISKDIR/daily_d7kwh
	fi
	if (( pvyieldcount == 34 )); then
		d8dailyyield=$(echo "scale=2;($d8 - $i) / 1000" |bc)
		echo $d8dailyyield > $RAMDISKDIR/daily_d8kwh
	fi
	if (( pvyieldcount == 35 )); then
		d9dailyyield=$(echo "scale=2;($d9 - $i) / 1000" |bc)
		echo $d9dailyyield > $RAMDISKDIR/daily_d9kwh
	fi
done
# now calculate the house consumption daily yield as difference of measured input and output
hausdailyyield=$(echo "scale=2;$bezugdailyyield + $pvdailyyield - $lladailyyield + $sedailyyield - $sidailyyield - $einspeisungdailyyield - $d1dailyyield - $d2dailyyield - $d3dailyyield - $d4dailyyield - $d5dailyyield - $d6dailyyield - $d7dailyyield - $d8dailyyield - $d9dailyyield - $verbraucher1dailyyield + $verbrauchere1dailyyield - $verbraucher2dailyyield + $verbrauchere2dailyyield - $verbraucher3dailyyield" | bc)
echo $hausdailyyield > $RAMDISKDIR/daily_hausverbrauchkwh

# get our current ip address
#ip route get 1 | awk '{print $NF;exit}' > $RAMDISKDIR/ipaddress
#prepare for Buster
ip route get 1 |  awk '{print $7;exit}' > $RAMDISKDIR/ipaddress

# check if our mqtt handler is running
if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/mqttsub.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 $OPENWBBASEDIR/runs/mqttsub.py &
fi

# check if our smarthome handler is running
if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/smarthomehandler.py" > /dev/null
then
	echo "test" > /dev/null
else
	python3 $OPENWBBASEDIR/runs/smarthomehandler.py >> $RAMDISKDIR/smarthome.log 2>&1 &
fi

# if this is a remote controlled system check if our isss handler is running
if (( isss == 1 )); then
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/isss.py" > /dev/null
	then
		echo "test" > /dev/null
	else
		python3 $OPENWBBASEDIR/runs/isss.py &
	fi
else
	ethstate=$(</sys/class/net/eth0/carrier)
	if (( ethstate == 1 )); then
		sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 up
		sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 down
		wlanstate=$(</sys/class/net/wlan0/carrier)
		if (( wlanstate == 1 )); then
			sudo systemctl stop hostapd
			sudo systemctl stop dnsmasq
		fi
	else
		sudo ifconfig wlan0:0 192.168.193.6 netmask 255.255.255.0 up
		sudo ifconfig eth0:0 192.168.193.5 netmask 255.255.255.0 down
	fi
fi

# if this is a socket system check for our handler to control the socket lock
if [[ "$evsecon" == "buchse" ]] && [[ "$isss" == "0" ]]; then
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/buchse.py" > /dev/null
	then
		echo "test" > /dev/null
	else
		python3 $OPENWBBASEDIR/runs/buchse.py &
	fi
fi

# if rfid mode 2 is configured check for our rfid handler
if [[ "$rfidakt" == "2" ]]; then
	echo $rfidlist > $RAMDISKDIR/rfidlist
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/rfid.py" > /dev/null
	then
		echo "test" > /dev/null
	else
		python3 $OPENWBBASEDIR/runs/rfid.py &
	fi
else
	if ps ax |grep -v grep |grep "python3 $OPENWBBASEDIR/runs/rfid.py" > /dev/null
	then
		sudo kill $(ps aux |grep 'runs/[r]fid.py' | awk '{print $2}')
	fi
fi

# check if our modbus server is running
if ps ax |grep -v grep |grep "sudo python3 $OPENWBBASEDIR/runs/modbusserver/modbusserver.py" > /dev/null
then
	echo "test" > /dev/null
else
	sudo python3 $OPENWBBASEDIR/runs/modbusserver/modbusserver.py &
fi

#Pingchecker
$OPENWBBASEDIR/runs/pingcheck.sh &

# truncate all logs in ramdisk
$OPENWBBASEDIR/runs/cleanup.sh >> $RAMDISKDIR/cleanup.log 2>&1
